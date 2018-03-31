from django.db import models
from django.conf import settings

from django.utils.timezone import now as tznow
from django.contrib.postgres.fields import JSONField
from enumfields import EnumIntegerField
from enumfields import Enum

class ArticleType(Enum):
    UNKNOWN = 0
    ESSAI = 1
    CHRONIQUE = 2
    CREATION = 3
    ENTRETIEN = 4
    LECTURE = 5
    SOMMAIRE_DOSSIER = 6

    class Labels:
        UNKNOWN = 'Inconnu'

class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET_DEFAULT, related_name='owned_articles', null=False, blank=False)
    created_on = models.DateTimeField('created date', auto_now_add=True, blank=False)
    published_on = models.DateTimeField('published date', default=tznow, null=False, blank=False)
    published = models.BooleanField(null=False, blank=False, default=False, db_index=True)

    html_file = models.FileField(upload_to='articles/', null=True, blank=True)
    id_senspublic = models.IntegerField(null=True, blank=True, unique=True, db_index=True)
    pdf_file = models.FileField(upload_to='articles/', null=True, blank=True)

    authors =  JSONField(null=True, blank=True)

    keywords = models.ManyToManyField('spkeyword.SPKeyword', related_name='articles', blank=True)
    type_article = EnumIntegerField(ArticleType, default=ArticleType.UNKNOWN)

    class Meta:
        permissions = (
            ('read_unpublished_articles', 'Can read unpublished articles'),
        )

    def get_absolute_url(self):
        return reverse('display_article', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
