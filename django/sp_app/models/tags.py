from django.db import models
from tagulous.models import TagModel, TagTreeModel
from enumfields import Enum, EnumField


class EditorTagsCategories(Enum):
    AUTHOR = 'Auteur'
    THEME = 'Thématique'


class EditorTag(TagModel):
    description = models.CharField(max_length=200, null=True, blank=True)
    link_rameau = models.URLField(null=True, blank=True)
    categorie = EnumField(EditorTagsCategories, max_length=1)

    class TagMeta:
        initial = "author/jamesbond, themes/histoire"
        force_lowercase = True
        space_delimiter = False
