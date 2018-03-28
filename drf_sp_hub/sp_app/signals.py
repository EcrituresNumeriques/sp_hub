import logging
import os
import re
from lxml import etree
import csv
import json
import time

from django.utils.html import strip_tags

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Article, SPKeyword, SPCategory, Conversation

from sp_app.lib.kw_matcher import KeywordMatcher

logger = logging.getLogger(__name__)

# Update keywords and article based on HTML file
@receiver(post_save, sender=Article)
def update_article_from_html_file(sender, instance, created, **kwargs):

    if not instance.html_file:
        return False

    id_senspublic = re.findall(r'SP(\d+).html', os.path.basename(instance.html_file.path))
    if len(id_senspublic) == 1:
        Article.objects.filter(pk=instance.pk).update(id_senspublic=id_senspublic[0])

    kw_matcher = KeywordMatcher(instance)
    # Clear keywords, then match and associate
    instance.keywords.clear()
    kw_matcher.match()

    # title = tree.xpath("//head/title")

    # if title and len(title) is 1:
    #    t = title[0].text
    #    logger.info('Updating title to ' + t)
    #    Article.objects.filter(pk=instance.pk).update(title=t)

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
    timestamp = time.time()

    if instance.pk is not None:
        orig = Conversation.objects.get(pk=instance.pk)
        message = 'modified'
        if orig.title != instance.title:
            message += ' title'
        if orig.keywords.all() != instance.keywords.all():
            message += ' keywords'
        if orig.articles.all() != instance.articles.all():
            message += ' articles'
        timeline = json.dumps(instance.timeline)
    else:
        message = 'created'
        timeline = json.dumps(data)

    data[timestamp] = message
    instance.timeline = dict(json.loads(timeline).items() | data.items())
