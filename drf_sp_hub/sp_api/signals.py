import logging
import os
import pprint
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from lxml import etree

from .models import Article, SPKeyword

# Update keywords and article based on HTML file
@receiver(post_save, sender=Article)
def update_spkeywords_from_article(sender, instance, created, **kwargs):
    logging.debug('RECEIVER POST SAVE')

    if not instance.html_file:
        logging.debug('No HTML file on this object')
        return False

    parser = etree.HTMLParser()
    tree = etree.parse(instance.html_file, parser)

    editor_keywords = tree.xpath("//meta[@name='controlledKeyword']")

    if not editor_keywords:
        return False

    instance.keywords.clear()
    for kw in editor_keywords:
        # Put the keys of the keyword in a set
        keys = set(kw.keys())
        if not set(['name', 'content', 'urirameau', 'idrameau', 'wikidata']).issubset(keys):
            # The keyword is not valid: skip it
            continue

        # Clear keywords first
        my_name = kw.get('content')

        if not my_name:
            logging.debug('Keyword looks empty?')
            logging.debug(kw)
            continue

        logging.debug('Found keyword: ' + my_name)

        my_data = {}
        is_aligned = 0
        aligned_fields = ['urirameau', 'idrameau', 'wikidata' ]
        for field in aligned_fields:
             content = kw.get(field)
             if content:
                 is_aligned = 1
                 my_data[field] = content

        existing_kw = SPKeyword.objects.filter(name=my_name)
        if existing_kw:
            existing_kw.update(data=my_data, aligned=is_aligned)
            logging.debug('Keyword ' + my_name + ' exists. Linking to ' + instance.title)
            instance.keywords.add(*existing_kw)
        else:
            logging.debug('Adding keyword ' + my_name)
            my_kw = SPKeyword.objects.create(name=my_name, data=my_data, aligned=is_aligned)
            my_kw.save()
            logging.debug('Linking keyword ' + my_name + ' to ' + instance.title)
            instance.keywords.add(my_kw)

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
