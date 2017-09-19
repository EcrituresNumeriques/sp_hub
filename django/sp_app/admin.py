from __future__ import unicode_literals

from django.contrib import admin

from .models import Article, Conversation, EditorTag, UserTag

class EditorTagAdmin(admin.ModelAdmin):
    fieldsets = (
        ( None, { 'fields': ('editor_tags', ) }),
    )

class UserTagAdmin(admin.ModelAdmin):
    fieldsets = (
        ( None, { 'fields': ('user_tags', ) }),
    )

# register our models in the admin site
admin.site.register(Conversation)
admin.site.register(Article)
admin.site.register(EditorTag, EditorTagAdmin)
admin.site.register(UserTag, UserTagAdmin)
