import logging
from django.db import models
from django.conf import settings

from django.contrib.postgres.fields import JSONField

class SPCategory(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True, unique=True)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'

class SPKeyword(models.Model):
    base_language = models.CharField(max_length=20, null=False, blank=False, default='fr')
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True, unique=True)
    data = JSONField(null=True, blank=True)
    aligned = models.BooleanField(null=False, blank=False, default=False)
    category = models.ForeignKey(SPCategory, unique=False, related_name='keywords', db_index=True, null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    def __str__(self):
        if self.category:
            return self.name + ' (' + self.category.name + ')'
        else:
            return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT, related_name='articles', null=False, blank=False)
    created_on = models.DateTimeField('published date', auto_now_add=True, blank=True)

    # Not yet
    html_file = models.FileField(upload_to='tmp/', null=True, blank=True)
    basex_docid = models.CharField(max_length=200, null=True, blank=True)
    keywords = models.ManyToManyField(SPKeyword, related_name='articles', blank=True)

    def __str__(self):
        return self.title + ' (ID ' + str(self.pk) + ')'

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT, null=True, blank=False, related_name='conversations')
    created_on = models.DateTimeField('published date', auto_now_add=True, blank=True)
    updated_on = models.DateTimeField('updated date', auto_now_add=True)

    articles = models.ManyToManyField(Article, blank=True, related_name='conversations')
    keywords = models.ManyToManyField(SPKeyword, blank=True, related_name='conversations')
    references = JSONField(null=True, blank=True)
    timeline = JSONField(null=False, blank=True)


    def __str__(self):
        return self.title + ' ' + str([ article.pk for article in self.articles.all() ])
