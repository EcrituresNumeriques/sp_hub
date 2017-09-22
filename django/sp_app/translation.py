from modeltranslation.translator import register, TranslationOptions
from .models import EditorTag

@register(EditorTag)
class EditorTagTranslationOptions(TranslationOptions):
    fields = ('name', )
