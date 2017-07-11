from django.db import models

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    published_date = models.DateTimeField('published date')

class Article(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    published_date = models.DateTimeField('published_date')
