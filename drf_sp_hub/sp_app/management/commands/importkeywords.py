from django.core.management.base import BaseCommand, CommandError

from sp_app.utils.spip_importer import SpipKeywords
from sp_app.utils.xml_importer import XMLKeywords
import os

class Command(BaseCommand):
    help = 'Import all keywords from XML and Spip'

    def handle(self, *args, **options):
        kw_match_xml = XMLKeywords('resources/groupes.xml')
        kw_match_xml.import_all()

        kw_match_spip = SpipKeywords('resources/spip_mots.csv')
        kw_match_spip.import_all()
