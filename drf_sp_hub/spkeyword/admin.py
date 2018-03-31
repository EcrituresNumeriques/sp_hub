from django.contrib import admin
from .models import SPKeyword, SPCategory

class ArticleInline(admin.TabularInline):
    model = 'Article.keywords.through'

class SPKeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_editor', 'aligned', 'language', 'is_translation')
    inlines = (ArticleInline, )

class SPCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')

admin.site.register(SPKeyword)
admin.site.register(SPCategory)
