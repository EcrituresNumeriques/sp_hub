from django.db import models
from django.conf import settings

class SpObject(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False)
    published_date = models.DateTimeField('published date', auto_now_add=True, blank=True)

    class Meta:
        abstract = True
