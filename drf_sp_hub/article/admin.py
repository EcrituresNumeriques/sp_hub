from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'html_file', 'pk', 'id_senspublic')

admin.site.register(Article, ArticleAdmin)
