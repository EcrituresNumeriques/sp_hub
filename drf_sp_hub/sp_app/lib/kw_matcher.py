import logging
import csv
import re
from lxml import etree

from django.utils.html import strip_tags

from sp_app.models import SPCategory
from sp_app.models import SPKeyword

logger = logging.getLogger(__name__)

class KeywordMatcher():

    def __init__(self, obj):
        self.parser = etree.HTMLParser()
        self.tree = etree.parse(obj.html_file, self.parser)
        self.instance = obj

    def match(self):
        if self.instance.html_file:
            self.associate_editor_keywords()
            self.associate_author_keywords()

    def associate_editor_keywords(self):
        """ Associates editor keywords with articles upon save """

        # https://github.com/timoguic/sp_hub/issues/31
        editor_keywords = self.tree.xpath("//div[@class='keywords']/div")

        for elem in editor_keywords:
            # <span property="subject" class="label">Imaginaire</span>
            kw_label = elem.xpath("span[@property='subject' and @class='label']")
            if not kw_label:
                continue

            kw_label = kw_label[0].text

            logger.info('Found editor keyword: ' + kw_label)

            kw_data = {}
            aligned_fields = ['urirameau', 'idrameau', 'wikidata' ]
            for field in aligned_fields:
                xpath_query = "span[@property='subject' and @class='{}']"
                alignment = elem.xpath(xpath_query.format(field))
                if alignment:
                    # We found an aligned field
                    kw_data[field] = alignment[0].text

            my_kw = create_update_editor_kw(kw_label, kw_data=kw_data, lang='fr')

            logger.info('Associating keyword ' + kw_label + ' to ' + self.instance.title)
            self.instance.keywords.add(my_kw)

    def associate_author_keywords(self):
        # <meta name="keywords" xml:lang="fr" lang="fr" content="Facebook, &#233;ditorialisation, algorithmes, connectivit&#233;, public, m&#233;dias, globalisation, opinion, bulle de filtre, segmentation." />
        author_keywords = self.tree.xpath("//meta[@name='keywords']")
        # TODO import keywords from other languages too

        for kw in author_keywords:
            lang = kw.get('lang')
            if not lang:
                lang = 'fr'

            label = kw.get('content')

            # We get rid of the possible ending '.'
            if label[len(label)-1] == '.':
                label = label[:-1]

            # Let's split on ;
            word_list = label.split(';')
            # No luck? We split on ,
            if len(word_list) == 1:
                word_list = ''.join(word_list).split(',')

            # Strip the words and their HTML tags
            word_list = [ strip_tags(w.strip()) for w in word_list ]

            for word in word_list:
                possible_kw = SPKeyword.objects.filter(name__iexact=word, language=lang, aligned=False)
                if possible_kw:
                    for kw in possible_kw:
                        logger.info('Linking ' + kw.name + ' to ' + str(self.instance.pk))
                        self.instance.keywords.add(kw)
                else:
                    logger.info('Creating ' + word)
                    my_kw = SPKeyword.objects.create(name=word, language=lang, aligned=False)
                    my_kw.save()
                    self.instance.keywords.add(my_kw)


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


""" HELPER FUNCTIONS"""

def create_update_keywords_from_multi_string(label, kw_data=None):
    # Do nothing if the string is empty
    if not label:
        return False

    created_keywords = []
    label_dict = split_multi_spstring(label)

    # Some keywords are multilingual but don't have French versions
    # So we check that first
    if 'fr' in label_dict:
        # Remove the french item from the dict
        kw_label = label_dict.pop('fr')
        # And create/update the corresponding keyword
        kw_fr = create_update_editor_kw(kw_label, kw_data=kw_data, lang='fr')
        created_keywords.append(kw_fr)

        # Then, look at other languages
        for lang in label_dict:
           new_kw = create_update_editor_kw(
            label_dict[lang],
            # We only have an alignemnt for the french version, so pass None here
            kw_data=None,
            lang=lang,
            translation_of=kw_fr,
           )
           created_keywords.append(new_kw)

        return created_keywords
    else:
        print("Cannot find 'fr' language for " + next(iter(label_dict.values())))
        return False

def create_update_editor_kw(label, kw_data=None, lang='fr', translation_of=None):
    # Look for an existing keyword by the same name
    existing_kw = SPKeyword.objects.filter(name=label, language=lang, is_editor=True)

    my_args = { 'is_editor': True,
                'language': lang,
                'is_translation': translation_of,
    }

    # If we have alignment info, then the keyword is aligned
    if kw_data:
        my_args['data'] = kw_data
        my_args['aligned'] = True

    # Update
    if existing_kw:
        logger.info('Update existing keyword: ' + label + ' (' + lang + ')')
        existing_kw.update(**my_args)
        return existing_kw.get()
    # Create
    else:
        logger.info('Create editor keyword ' + label + ' (' + lang + ')')
        my_kw = SPKeyword.objects.create(name=label, **my_args)
        my_kw.save()
        return my_kw

def split_multi_spstring(s):
    # Look for multilingual patterns
    matches = re.findall('\[(..)\]([^\[<]+)', s)
    # Looks like it's not multilingual
    if not matches:
        return { 'fr': s }
    else:
        return { m[0]: m[1] for m in matches }
