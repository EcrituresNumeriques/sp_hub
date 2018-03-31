from lxml import etree

from .func_importer import create_update_keywords_from_multi_string

import logging
logger = logging.getLogger(__name__)

class XMLKeywords():
    # Class variables (namespaces)
    sp_ns = 'http://sens-public.org/sp/'
    namespaces = { 'ns': sp_ns }

    def __init__(self, file_path):
        # Init XML parser
        parser = etree.XMLParser()
        tree = etree.parse(file_path, parser)
        # Get <entry> elements
        self.results = tree.xpath('//ns:entry', namespaces=self.namespaces)

    def import_all(self):
        logger.info('========== IMPORT XML =========')
        # For multilingual entries (<multi>[fr]Bla[en]Blah</multi>)
        multi_with_ns = '{' + self.sp_ns + '}' + 'multi'

        id_with_ns = '{' + self.sp_ns + '}' + 'id'
        url_with_ns = '{' + self.sp_ns + '}' + 'url'

        for r in self.results:
            # Find ID Rameau of the keyword
            kw_id = r.find(id_with_ns)
            # Find URL rameau of the keyword
            kw_url = r.find(url_with_ns)

            if kw_id is None or kw_url is None:
                continue

            # Look for a label
            label = r.xpath('ns:label', namespaces=self.namespaces)
            if len(label) == 0:
                # This is not good. Probably better to skip
                continue

            label_dict = {}

            if isinstance(label, list) and len(label) > 0:
                children = label[0].find(multi_with_ns)
                # We found a <multi> element - retrieve its text content
                if children is not None:
                    label = children.text
                else:
                    # No multi - get the text of the label element
                    label = label[0].text
            else:
                # In the worst case, the text could be there already
                label = label.text

            kw_data = {}
            kw_data['idrameau'] = kw_id.text
            kw_data['urlrameau'] = kw_url.text

            create_update_keywords_from_multi_string(label, kw_data)
