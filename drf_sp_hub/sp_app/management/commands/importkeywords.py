from django.core.management.base import BaseCommand, CommandError
from sp_app.models import SPKeyword

from sp_app.lib.kw_matcher import XMLKeywords, SpipKeywords

import os

class Command(BaseCommand):
    help = 'Import all keywords from XML and Spip'

    def handle(self, *args, **options):
        kw_match_xml = XMLKeywords('resources/groupes.xml')
        kw_match_xml.import_all()

        kw_match_spip = SpipKeywords('resources/spip_mots.csv')
        kw_match_spip.import_all()
