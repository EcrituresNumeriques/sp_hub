from django.db import models
from .sp_object import SpObject
from .article import Article

class Conversation(SpObject):
    articles = models.ManyToManyField(Article, blank=True)

    def __str__(self):
        return self.title + ' ' + str([ article.pk for article in self.articles.all() ])
