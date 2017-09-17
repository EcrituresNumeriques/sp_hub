import os
import requests

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from .sp_constants import Constants

class SpObject(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, blank=False)
    published_date = models.DateTimeField('published date', auto_now_add=True, blank=True)

    class Meta:
        abstract = True

class Conversation(SpObject):
    pass

class Article(SpObject):
    document = models.FileField(upload_to='tmp/', null=True, blank=True)
    basex_docid = models.CharField(max_length=  200, null=True, blank=True)

    def __unicode__(self):
        return title + '(' + basex_docid + ')'


@receiver(post_save, sender=Article)
def upload_to_basex(sender, instance, created, **kwargs):
    if instance.document and created:
        file_contents = instance.document.storage.open(instance.document.name, 'r').read()

        if file_contents:
            basex_id = str(instance.pk) + '.html'
            rest_url = Constants.BASEX_REST_URL + '/' + Constants.BASEX_DB \
                + '/' + basex_id
            print('Calling PUT ' + rest_url)
            r = requests.put(rest_url,
                auth=('admin', 'admin'),
                data=file_contents,
                headers={ 'Content-type': 'text/html', 'Accept': 'text/html' },
            )
            print(str(r.status_code) + ' ' + r.text)
            if(r.status_code == 201):
                instance.basex_docid = basex_id
                instance.save()

@receiver(pre_delete, sender=Article)
def delete_basex_document(sender, instance, **kwargs):
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)

        rest_url = Constants.BASEX_REST_URL + '/' + Constants.BASEX_DB \
            + '/' + instance.basex_docid
        print('Calling DELETE ' + rest_url)
        r = requests.delete(rest_url,
            auth=('admin', 'admin'),
        )
        print(str(r.status_code) + ' ' + r.text)

    #print(instance.document.storage.open('tmp/' + instance.document.name, 'r').read())
