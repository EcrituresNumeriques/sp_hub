import logging
import csv
import re
import json

from lxml import etree

from django.utils.html import strip_tags

from article.models import Article
from spkeyword.models import SPKeyword, SPCategory

from .func_importer import create_update_editor_kw

import logging
logger = logging.getLogger(__name__)

class HTMLImporter():

    def __init__(self, obj):
        self.parser = etree.HTMLParser()
        self.tree = etree.parse(obj.html_file, self.parser)
        self.instance = obj

    def process_file(self):
        if self.instance.html_file:
            self.update_authors_field()
            self.associate_editor_keywords()
            self.associate_author_keywords()
            self.associate_dossier()

    def associate_dossier(self):
        # <span property="isPartOf" typeof="PublicationVolume" resource="#periodical" class="titreDossier">Ontologie du num&#233;rique</span>
        info_dossier = self.tree.xpath("//span[@property='isPartOf' and @class='titreDossier']")
        if info_dossier:
            for d in info_dossier:
                dossier_title = d.text
                dossier_obj = Dossier.objects.get_or_create(title=dossier_title)
                self.instance.dossiers.add(dossier_obj)

    def update_authors_field(self):
        authors = self.tree.xpath("//div[@vocab='http://xmlns.com/foaf/0.1/' and @typeof='Person' and @class='foaf-author']")
        author_dict = dict()
        for a in authors:
            nom = a.xpath("span[@property='familyName']")

            if not nom:
                continue
            else:
                if not nom[0].text:
                    continue

            nom = nom[0].text

            prenom = a.xpath("span[@property='firstName']")
            if prenom:
                nom = nom + ' ' + prenom[0].text

            orcid = a.xpath("span[@property='openid']")
            if orcid:
                orcid = orcid[0].text

            author_dict[nom] = orcid

        Article.objects.filter(pk=self.instance.pk).update(authors=json.dumps(author_dict))

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
            aligned_fields = ['uriRameau', 'idRameau', 'wikidata' ]
            for field in aligned_fields:
                xpath_query = "span[@property='subject' and @class='{}']"
                alignment = elem.xpath(xpath_query.format(field))
                if alignment:
                    # We found an aligned field
                    if alignment[0].text:
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
