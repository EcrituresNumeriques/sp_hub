import logging
import os
from lxml import etree
import csv

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Article, SPKeyword

# Update keywords and article based on HTML file
@receiver(post_save, sender=Article)
def update_spkeywords_from_article(sender, instance, created, **kwargs):
    logging.debug('RECEIVER POST SAVE')

    if not instance.html_file:
        logging.debug('No HTML file on this object')
        return False

    # Init HTML parser
    parser = etree.HTMLParser()
    tree = etree.parse(instance.html_file, parser)

    # <meta name="controlledKeyword" content="Freud, Sigmund" uriRameau="http://catalogue.bnf.fr/ark:/12148/cb119035855" idRameau="FRBNF11903585" wikidata="https://www.wikidata.org/wiki/Q9215" />
    editor_keywords = tree.xpath("//meta[@name='controlledKeyword']")
    # <meta name="keywords" xml:lang="fr" lang="fr" content="Facebook, &#233;ditorialisation, algorithmes, connectivit&#233;, public, m&#233;dias, globalisation, opinion, bulle de filtre, segmentation." />
    author_keywords = tree.xpath("//meta[@name='keywords' and @lang='fr']")

    if editor_keywords or author_keywords:
        # Clear keywords first
        instance.keywords.clear()

    match_and_associate_editor_keywords(instance, editor_keywords)
    match_and_associate_author_keywords(instance, author_keywords)


def match_and_associate_editor_keywords(obj, editor_kw):
    # Init keyword matcher
    kw_matcher = KeywordMatcherFromSpip('resources/spip_mots.csv')

    for kw in editor_kw:
        my_name = kw.get('content')

        if not my_name:
            # Empty keyword
            continue

        logging.debug('Found keyword: ' + my_name)

        my_data = {}
        # By default, keywords are not aligned
        is_aligned = False
        aligned_fields = ['urirameau', 'idrameau', 'wikidata' ]
        for field in aligned_fields:
             content = kw.get(field)
             if content:
                 # We found an aligned field
                 is_aligned = True
                 my_data[field] = content

        my_args = { 'data': my_data, 'aligned': is_aligned }

        # Search for the parent category in the matcher
        parent_cat = kw_matcher.find_parent(my_name)
        if not parent_cat > 0:
            parent_cat = None

        my_args['parent_category'] = parent_cat

        existing_kw = SPKeyword.objects.filter(name=my_name)
        if existing_kw:
            existing_kw.update(**my_args)
            logging.debug('Keyword ' + my_name + ' exists. Linking to ' + obj.title)
            obj.keywords.add(*existing_kw)
        else:
            logging.debug('Adding keyword ' + my_name)
            my_kw = SPKeyword.objects.create(name=my_name, **my_args)
            my_kw.save()
            logging.debug('Linking keyword ' + my_name + ' to ' + obj.title)
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

        word_list = [ w.strip() for w in word_list ]
        for word in word_list:
            possible_kw = SPKeyword.objects.filter(name__iexact=word)
            if possible_kw:
                logging.debug(word + ' looks like ' + possible_kw.get().name + '. Linking.')
                obj.keywords.add(possible_kw.get())
            else:
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
        self.data = {}
        for row in csvreader:
            cat_name = row[1]
            parent_name = row[5]
            if row[1].rfind('[fr]') > 0:
                cat_name = row[1].split('[fr]')[1].split('[')[0]
            self.data[cat_name] = parent_name
            logging.debug(self.data)

    def find_parent(self, name):
        if name in self.data.keys():
            parent_name = self.data[name]
            if parent_name:
                # Does this keyword exist?
                existing_kw = SPKeyword.objects.filter(name=parent_name)
                if existing_kw:
                    logging.debug('Found existing parent!' + str(existing_kw.get().id))
                    return existing_kw.get().id
                else:
                    logging.debug('Creating parent: ' + parent_name)
                    my_kw = SPKeyword.objects.create(name=parent_name)
                    my_kw.save()
                    return my_kw.id
        else:
            return False
