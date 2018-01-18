import logging
import csv

from django.utils.html import strip_tags

from sp_app.models import SPCategory
from sp_app.models import SPKeyword

logger = logging.getLogger(__name__)

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

    def associate_author_keywords(self, obj, author_kw):
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

    def associate_editor_keywords(self, obj, editor_kw):
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
            parent_cat = self.find_parent(my_name)
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
