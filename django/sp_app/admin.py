from __future__ import unicode_literals

from django.contrib import admin

from .models import Article, Conversation, EditorTag

admin.site.register(Conversation)
admin.site.register(Article)
admin.site.register(EditorTag)
