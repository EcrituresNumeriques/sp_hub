from django.db import models

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
        return reverse('spkeyword:display', kwargs={'pk': self.pk})

    def __str__(self):
        if self.category:
            return self.category.name + ': ' + self.name
        else:
            return self.name
