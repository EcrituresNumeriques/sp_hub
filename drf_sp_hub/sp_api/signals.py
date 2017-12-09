
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article, Conversation

from lxml import etree

@receiver(post_save, sender=Article)
def update_spkeywords_from_article(sender, instance, created, **kwargs):
    instance.html_file.read()

    parser = etree.HTMLParser()
    tree = etree.parse(html_contents, parser)

    editor_keywords = tree.xpath("//meta[@name='controlledKeyword']")

    for kw in keywords:
        # Put the keys of the keyword in a set
        keys = set(kw.keys())
        if not set(['name', 'content', 'urirameau', 'idrameau', 'wikidata']).issubset(keys):
            # The keyword is not valid: skip it
            continue

        print(kw.items())
