import logging
import os
from lxml import etree
import csv
import json
import time

from django.utils.html import strip_tags

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Article, SPKeyword, SPCategory, Conversation
from sp_app.lib.kw_matcher import KeywordMatcherFromSpip

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
        kw_matcher = KeywordMatcherFromSpip('resources/spip_mots.csv')
        # Match and associate
        kw_matcher.associate_editor_keywords(instance, editor_keywords)
        kw_matcher.associate_author_keywords(instance, author_keywords)

    if title and len(title) is 1:
        t = title[0].text
        logger.info('Updating title to ' + t)
        Article.objects.filter(pk=instance.pk).update(title=t)

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

@receiver(pre_save, sender=Conversation)
def update_timeline_before_save(sender, instance, **kwargs):
    data = {}
    data[time.time()] = 'modified'
    if not instance.timeline or instance.timeline == 'null':
        instance.timeline = json.dumps(data)
    else:
        if isinstance(instance.timeline, dict):
            instance.timeline = json.dumps(instance.timeline)
        instance.timeline = dict(json.loads(instance.timeline).items() | data.items())
