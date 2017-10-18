from django.contrib.postgres.fields import JSONField

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .article import Article
from .spkeyword import SPKeyword
import time

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False)
    published_date = models.DateTimeField('published date', auto_now_add=True, blank=True)
    articles = models.ManyToManyField(Article, blank=True, related_name='conversations')
    keywords = models.ManyToManyField(SPKeyword, blank=True)
    references = JSONField(null=True, blank=False, default={})
    timeline = JSONField(null=False, blank=False, default={})


    def __str__(self):
        return self.title + ' ' + str([ article.pk for article in self.articles.all() ])

    def save(self, *args, **kwargs):
        if 'form' in kwargs:
            form = kwargs['form']
        else:
            form = None

        self.conversation_update_timeline(form)

        super(Conversation, self).save(*args, **kwargs)

    def conversation_update_timeline(self, form):
        timestamp = int(time.time())
        action = 'updated'
        self.timeline.update({ timestamp: { 'action': 'nothing', 'user': 'test' } })
