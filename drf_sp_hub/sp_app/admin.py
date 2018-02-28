from django.contrib import admin

from .models import Article, Conversation, SPKeyword, SPCategory

class ArticleInline(admin.TabularInline):
    model = Article.keywords.through

class SPKeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_editor', 'aligned', 'language', 'is_translation')
    inlines = (ArticleInline, )

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'html_file', 'pk', 'id_senspublic')

class SPCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')

admin.site.register(Conversation)
admin.site.register(Article, ArticleAdmin)
admin.site.register(SPKeyword, SPKeywordAdmin)
admin.site.register(SPCategory, SPCategoryAdmin)
