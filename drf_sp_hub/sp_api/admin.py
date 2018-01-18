from django.contrib import admin

from .models import Article, Conversation, SPKeyword, SPCategory

class SPKeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_editor', 'aligned')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'html_file', 'pk')

admin.site.register(Conversation)
admin.site.register(Article, ArticleAdmin)
admin.site.register(SPKeyword, SPKeywordAdmin)
admin.site.register(SPCategory)
