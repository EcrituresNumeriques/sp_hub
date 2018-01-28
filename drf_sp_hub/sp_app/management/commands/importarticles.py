from django.core.management.base import BaseCommand, CommandError
from sp_app.models import Article, SPKeyword, SPCategory

from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Import all HTML articles in the resources/ folder'

    def handle(self, *args, **options):
        print('Cleaning all articles from the DB...')
        Article.objects.all().delete()
        for f in os.listdir('resources/html'):
            if f.startswith('SP') and f.endswith('.html'):
                print('Found file ' + f + '! Processing...')
                fp = open(os.path.join('resources/html', f), 'rb')
                a = Article.objects.create(title=f)
                a.html_file.save(f, File(fp))
