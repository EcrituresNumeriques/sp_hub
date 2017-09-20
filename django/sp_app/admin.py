from __future__ import unicode_literals

from django.contrib import admin
import tagulous.admin

from .models import Article, Conversation, EditorTag

class EditorTagAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'description' ]

admin.site.register(Conversation)
admin.site.register(Article)
tagulous.admin.register(EditorTag, EditorTagAdmin)
