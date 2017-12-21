from django.contrib import admin

from .models import Article, Conversation, SPKeyword, SPCategory

admin.site.register(Conversation)
admin.site.register(Article)
admin.site.register(SPKeyword)
admin.site.register(SPCategory)
