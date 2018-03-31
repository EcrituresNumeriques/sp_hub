from django.db import models
from django.conf import settings

from django.urls import reverse

from django.utils.timezone import now as tznow

from enumfields import EnumIntegerField
from enumfields import Enum

from django.contrib.postgres.fields import JSONField

class Dossier(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    redacteurs = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    sommaire = models.ForeignKey('article.Article', null=True, blank=True, on_delete=models.SET_NULL)
    articles = models.ManyToManyField('article.Article', blank=True, related_name='dossiers', through='DossierOrder')

class DossierOrder(models.Model):
    order = models.PositiveIntegerField()
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT, null=True, blank=False, related_name='conversations')
    created_on = models.DateTimeField('published date', auto_now_add=True, blank=True)
    updated_on = models.DateTimeField('updated date', auto_now_add=True)

    articles = models.ManyToManyField('article.Article', blank=True, related_name='conversations')
    keywords = models.ManyToManyField('spkeyword.SPKeyword', blank=True, related_name='conversations')
    references = JSONField(null=True, blank=True)
    timeline = JSONField(null=False, blank=True)

    def get_absolute_url(self):
        return reverse('sp_app:display_conversation', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
