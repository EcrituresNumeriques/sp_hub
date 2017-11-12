from django.db import models
from django.conf import settings

from django.contrib.postgres.fields import JSONField

class SPKeyword(models.Model):
    base_language = models.CharField(max_length=20, null=False, blank=False, default='fr')
    data = JSONField()
    aligned = models.IntegerField(null=True, blank=False, default=0)


    def __str__(self):
        print(self.base_language)
        if(self.data):
            return str(self.data[self.base_language]['title'])
        else:
            return 'base lang undefined'

class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='articles', null=False, blank=False)
    created_on = models.DateTimeField('published date', auto_now_add=True, blank=True)

    # Not yet
    # document = models.FileField(upload_to='tmp/', null=True, blank=True)
    basex_docid = models.CharField(max_length=200, null=True, blank=True)
    keywords = models.ManyToManyField(SPKeyword, related_name='articles', blank=True)

    def __str__(self):
        return self.title + ' (' + str(self.pk) + '.html)'

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False, related_name='conversations')
    created_on = models.DateTimeField('published date', auto_now_add=True, blank=True)
    updated_on = models.DateTimeField('updated date', auto_now_add=True)
    articles = models.ManyToManyField(Article, blank=True, related_name='conversations')
    keywords = models.ManyToManyField(SPKeyword, blank=True, related_name='conversations')
    references = JSONField(null=True, blank=True)
    timeline = JSONField(null=False, blank=True)


    def __str__(self):
        return self.title + ' ' + str([ article.pk for article in self.articles.all() ])

