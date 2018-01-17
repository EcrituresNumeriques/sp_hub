from django.core.management.base import BaseCommand, CommandError
from sp_api.models import Article, SPKeyword, SPCategory

from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Deletes all objects from the DB!'

    def handle(self, *args, **options):
        print('Cleaning all articles from the DB...')
        Article.objects.all().delete()
        print('Cleaning all keywords and categories from the DB...')
        SPKeyword.objects.all().delete()
        SPCategory.objects.all().delete()
