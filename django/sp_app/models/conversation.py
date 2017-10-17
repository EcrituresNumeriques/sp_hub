from django.conf import settings
from django.db import models
from .article import Article

class Conversation(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False)
    published_date = models.DateTimeField('published date', auto_now_add=True, blank=True)
    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.title + ' ' + str([ article.pk for article in self.articles.all() ])
