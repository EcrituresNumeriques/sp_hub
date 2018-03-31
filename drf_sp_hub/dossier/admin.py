from django.contrib import admin

from .models import Dossier

class ArticleInline(admin.TabularInline):
    model = Dossier.articles.through

class DossierAdmin(admin.ModelAdmin):
    inlines = (
        ArticleInline,
    )

admin.site.register(Dossier, DossierAdmin)
