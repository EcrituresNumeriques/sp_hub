from django.contrib.postgres.fields import JSONField
from django.db import models

from enumfields import Enum, EnumField


class KeywordType(Enum):
    AUTHOR = 'Auteur'
    EDITOR = 'Editor'

class SPKeyword(models.Model):
    kw_type = EnumField(KeywordType, default=KeywordType.AUTHOR)
    base_language = models.CharField(max_length=20, null=False, blank=False, default='fr')
    data = JSONField()
    aligned = models.IntegerField(null=True, blank=False, default=0)


    def __str__(self):
        print(self.base_language)
        if(self.data):
            return str(self.data[self.base_language]['title'])
        else:
            return 'base lang undefined'
