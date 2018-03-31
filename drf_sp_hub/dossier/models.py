from django.db import models
from django.conf import settings

class Dossier(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    redacteurs = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    sommaire = models.ForeignKey('article.Article', null=True, blank=True, on_delete=models.SET_NULL)
    articles = models.ManyToManyField('article.Article', blank=True, related_name='dossiers', through='DossierOrder')

class DossierOrder(models.Model):
    order = models.PositiveIntegerField()
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)
