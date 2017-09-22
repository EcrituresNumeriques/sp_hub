from django.db import models
#from tagulous.models import TagModel, TagTreeModel

#from enumfields import Enum, EnumField


#class EditorTagsCategories(Enum):
#    AUTHOR = 'Auteur'
#    THEME = 'Thématique'

class EditorTag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    id_spip = models.IntegerField(null=True, blank=True)
    link_rameau = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
