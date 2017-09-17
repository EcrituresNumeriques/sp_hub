from __future__ import unicode_literals

from django.contrib import admin

from .models import Conversation, Article

# register our models in the admin site
admin.site.register(Conversation)
admin.site.register(Article)
