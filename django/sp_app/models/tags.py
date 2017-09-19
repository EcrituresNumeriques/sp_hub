from django.db import models
from taggit.models import TagBase, TaggedItemBase


class EditorTag(TagBase):
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Tag éditeur"
        verbose_name_plural = "Tags éditeur"


class EditorTaggedArticle(TaggedItemBase):
    content_object = models.ForeignKey('Article')
    tag = models.ForeignKey(EditorTag, related_name="%(app_label)s_%(class)s_items")


class UserTag(TagBase):
    description = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Tag user"
        verbose_name_plural = "Tags user"


class UserTaggedArticle(TaggedItemBase):
    content_object = models.ForeignKey('Article')
    tag = models.ForeignKey(UserTag, related_name="%(app_label)s_%(class)s_items")
