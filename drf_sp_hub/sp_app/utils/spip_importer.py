import csv

from spkeyword.models import SPKeyword, SPCategory
from .func_importer import create_update_keywords_from_multi_string

import logging
logger = logging.getLogger(__name__)

class SpipKeywords():

    def __init__(self, file_path):
        csvfile = open(file_path, encoding='utf-8')
        # Skip first line
        csvfile.readline()
        self.csvreader = csv.reader(csvfile, delimiter=';')

    def import_all(self):
        logger.info('========== IMPORT SPIP =========')
        for row in self.csvreader:
            label = row[1]
            parent_name = row[5]

            if parent_name:
                logger.info('Category ' + parent_name)
                my_cat = SPCategory.objects.get_or_create(name=parent_name)

            if label:
                my_keywords = create_update_keywords_from_multi_string(label)

                # Associate parents
                for k in my_keywords:
                    logger.info('Update keyword ' + k.name + ' with parent ' + my_cat[0].name)
                    k.category = my_cat[0]
                    k.save()
