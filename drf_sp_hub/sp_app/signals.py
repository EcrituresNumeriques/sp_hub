import logging
import os
from lxml import etree
import csv

from django.utils.html import strip_tags

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Article, SPKeyword, SPCategory

logger = logging.getLogger(__name__)

# Update keywords and article based on HTML file
@receiver(post_save, sender=Article)
def update_article_from_html_file(sender, instance, created, **kwargs):

    if not instance.html_file:
        return False

    # Init HTML parser
    parser = etree.HTMLParser()
    tree = etree.parse(instance.html_file, parser)

    # <meta name="controlledKeyword" content="Freud, Sigmund" uriRameau="http://catalogue.bnf.fr/ark:/12148/cb119035855" idRameau="FRBNF11903585" wikidata="https://www.wikidata.org/wiki/Q9215" />
    editor_keywords = tree.xpath("//meta[@name='controlledKeyword']")
    # <meta name="keywords" xml:lang="fr" lang="fr" content="Facebook, &#233;ditorialisation, algorithmes, connectivit&#233;, public, m&#233;dias, globalisation, opinion, bulle de filtre, segmentation." />
    author_keywords = tree.xpath("//meta[@name='keywords' and @lang='fr']")
    title = tree.xpath("//head/title")

    if editor_keywords or author_keywords:
        # Clear keywords first
        instance.keywords.clear()
        # Match and associate
        match_and_associate_editor_keywords(instance, editor_keywords)
        match_and_associate_author_keywords(instance, author_keywords)

    if title and len(title) is 1:
        t = title[0].text
        logger.info('Updating title to ' + t)
        Article.objects.filter(pk=instance.pk).update(title=t)


def match_and_associate_editor_keywords(obj, editor_kw):
    # Init keyword matcher
    kw_matcher = KeywordMatcherFromSpip('resources/spip_mots.csv')

    for kw in editor_kw:
        my_name = kw.get('content')
        if not my_name:
            # Empty keyword
            continue

        logger.info('Found editor keyword: ' + my_name)

        my_data = {}
        # By default, keywords are not aligned - but these are editors'
        is_aligned = False
        is_editor = True
        aligned_fields = ['urirameau', 'idrameau', 'wikidata' ]
        for field in aligned_fields:
             content = kw.get(field)
             if content:
                 # We found an aligned field
                 is_aligned = True
                 my_data[field] = content

        my_args = { 'data': my_data, 'aligned': is_aligned, 'is_editor': is_editor }

        # Search for the parent category in the matcher
        parent_cat = kw_matcher.find_parent(my_name)
        if parent_cat:
            logger.info('Found parent category: ' + parent_cat.name)
            my_args['category'] = parent_cat

        # Check for an existing keyword already in the database
        existing_kw = SPKeyword.objects.filter(name=my_name)
        if existing_kw:
            existing_kw.update(**my_args)
            logger.info('Editor keyword ' + my_name + ' exists. Linking to ' + obj.title)
            # We use * just in case we have a list
            obj.keywords.add(*existing_kw)
        else:
            logger.info('Creating editor keyword ' + my_name)
            my_kw = SPKeyword.objects.create(name=my_name, **my_args)
            my_kw.save()
            logger.info('Linking editor keyword ' + my_name + ' to ' + obj.title)
            obj.keywords.add(my_kw)

def match_and_associate_author_keywords(obj, author_kw):
    for kw in author_kw:
        # <meta name="keywords" xml:lang="fr" lang="fr" content="Facebook, &#233;ditorialisation, algorithmes, connectivit&#233;, public, m&#233;dias, globalisation, opinion, bulle de filtre, segmentation." />
        my_value = kw.get('content')

        # We get rid of the possible ending '.
        if my_value[len(my_value)-1] == '.':
            my_value = my_value[:-1]

        # Let's split on ;
        word_list = my_value.split(';')
        # No luck? We split on ,
        if len(word_list) == 1:
            word_list = ''.join(word_list).split(',')

        # Strip the words
        word_list = [ strip_tags(w.strip()) for w in word_list ]
        logger.info('Author keywords found:' + ','.join(word_list))
        for word in word_list:
            possible_kw = SPKeyword.objects.filter(name__iexact=word, aligned=False)
            if possible_kw:
                for kw in possible_kw:
                    logger.info(word + ' ~ ' + kw.name + '. Linking.')
                    obj.keywords.add(kw)
            else:
                logger.info('Creating ' + word)
                my_kw = SPKeyword.objects.create(name=word)
                my_kw.save()
                obj.keywords.add(my_kw)

# Deletes associated files when object is deleted
@receiver(post_delete, sender=Article)
def delete_html_file_on_delete(sender, instance, **kwargs):
    if instance.html_file:
        if os.path.isfile(instance.html_file.path):
            os.remove(instance.html_file.path)

@receiver(pre_save, sender=Article)
def delete_html_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Article.objects.get(pk=instance.pk).html_file
    except Article.DoesNotExist:
        return False

    new_file = instance.html_file
    if old_file and not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class KeywordMatcherFromSpip:
    def __init__(self, file_path):
        csvfile = open(file_path, encoding='utf-8')
        csvreader = csv.reader(csvfile, delimiter=';')
        self.parent_cat = {}
        for row in csvreader:
            cat_name = row[1]
            parent_name = row[5]
            if row[1].rfind('[fr]') > 0:
                cat_name = row[1].split('[fr]')[1].split('[')[0]
            self.parent_cat[cat_name] = parent_name

    def find_parent(self, name):
        if name in self.parent_cat.keys():
            parent_name = self.parent_cat[name]
            if parent_name:
                # Does this keyword exist?
                existing_cat = SPCategory.objects.filter(name=parent_name)
                if existing_cat:
                    existing_cat = existing_cat.get()
                    logger.info('Found existing parent category: ' + existing_cat.name + ' (' + str(existing_cat.id) + ')')
                    return existing_cat
                else:
                    logger.info('Creating parent cat: ' + parent_name)
                    my_kw = SPCategory.objects.create(name=parent_name)
                    my_kw.save()
                    return my_kw
        else:
            return False
