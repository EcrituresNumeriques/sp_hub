from django.db import models
from django.conf import settings

from django.urls import reverse

from django.utils.timezone import now as tznow

from enumfields import EnumIntegerField
from enumfields import Enum

from django.contrib.postgres.fields import JSONField

class SPCategory(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True, unique=True)

    class Meta:
        verbose_name = "SP Category"
        verbose_name_plural = "SP Categories"

    def __str__(self):
        return self.name

class SPKeyword(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, db_index=True)
    language = models.CharField(max_length=3, null=False, blank=False, default='fr')
    is_translation = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='translations',
        on_delete=models.SET_NULL,
        limit_choices_to={'language': 'fr'},
    )
    data = JSONField(null=True, blank=True)
    aligned = models.BooleanField(null=False, blank=False, default=False)
    is_editor = models.BooleanField(null=False, blank=False, default=False)
    category = models.ForeignKey(SPCategory, unique=False, related_name='keywords', db_index=True, null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "SP Keyword"

    def get_absolute_url(self):
        return reverse('sp_app:display_keyword', kwargs={'pk': self.pk})

    def __str__(self):
        if self.category:
            return self.category.name + ': ' + self.name
        else:
            return self.name

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
        SOMMAIRE_DOSSIER = 'Sommaire dossier'

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
    
    keywords = models.ManyToManyField(SPKeyword, related_name='articles', blank=True)
    type_article = EnumIntegerField(ArticleType, default=ArticleType.UNKNOWN)

    class Meta:
        permissions = (
            ('can_view_unpublished_article', 'Can read unpublished article'),
        )

    def get_absolute_url(self):
        return reverse('display_article', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Dossier(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    redacteurs = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    sommaire = models.ForeignKey(Article, null=True, blank=True, on_delete=models.SET_NULL)
    articles = models.ManyToManyField(Article, blank=True, related_name='dossiers', through='DossierOrder')

class DossierOrder(models.Model):
    order = models.PositiveIntegerField()
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

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

    def get_absolute_url(self):
        return reverse('sp_app:display_conversation', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
