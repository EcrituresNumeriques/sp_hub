import logging

import json
import time

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Conversation

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
