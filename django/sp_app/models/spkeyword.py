from django.contrib.postgres.fields import JSONField
from django.db import models

from enumfields import Enum, EnumField


class KeywordType(Enum):
    AUTHOR = 'Auteur'
    EDITOR = 'Editor'

class SPKeyword(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    kw_type = EnumField(KeywordType, default=KeywordType.AUTHOR)
    description = models.CharField(max_length=200, null=True, blank=True)
    aligned = models.IntegerField(null=True, blank=False, default=0)
    data = JSONField()

    def __str__(self):
        return self.name
