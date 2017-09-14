from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class SpObject(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False)
    published_date = models.DateTimeField('published date', auto_now_add=True, blank=True)

    class Meta:
        abstract = True

class Conversation(SpObject):
    pass


class Article(SpObject):
    document = models.FileField(upload_to='tmp/', null=True, blank=True)
    basex_docid = models.IntegerField(null=True, blank=True)
