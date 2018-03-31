from django.db import models
from django.conf import settings

class Dossier(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    redacteurs = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    articles = models.ManyToManyField('article.Article', blank=True, related_name='dossiers', through='DossierOrder')

    def __str__(self):
        return self.title

class DossierOrder(models.Model):
    order = models.PositiveIntegerField(null=False, default=1)
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    article = models.ForeignKey('article.Article', on_delete=models.CASCADE)
    sommaire = models.BooleanField(null=False, default=False)
