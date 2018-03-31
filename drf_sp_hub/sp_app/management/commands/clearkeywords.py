from django.core.management.base import BaseCommand, CommandError
from spkeyword.models import SPKeyword, SPCategory

import os

class Command(BaseCommand):
    help = 'Clear all keywords and categories'

    def handle(self, *args, **options):
        SPKeyword.objects.all().delete()
