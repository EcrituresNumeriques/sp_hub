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
    # document will be stored on sp_hub too, just in case...
    document = models.FileField(upload_to='tmp/', null=True, blank=True)
    # field to reference the ID of the document in BaseX
    basex_docid = models.CharField(max_length=  200, null=True, blank=True)

    def __str__(self):
        return title + '(' + basex_docid + ')'

# this method is called after an object is saved
@receiver(post_save, sender=Article)
def upload_to_basex(sender, instance, created, **kwargs):
    # if the user provided a file for upload
    if instance.document:
        # try to open the file
        file_contents = instance.document.storage.open(instance.document.name, 'r').read()

        if file_contents:
            # id in BaseX = id in sp_hub + .html
            basex_id = str(instance.pk) + '.html'
            # URL to store the document
            rest_url = Constants.BASEX_REST_URL + '/' + Constants.BASEX_DB \
                + '/' + basex_id
            print('Calling PUT ' + rest_url)
            r = requests.put(rest_url,
                auth=Constants.BASEX_CREDENTIALS,
                data=file_contents,
                headers={ 'Content-type': 'text/html', 'Accept': 'text/html' },
            )
            print(str(r.status_code) + ' ' + r.text)
            if(r.status_code == 201):
                # Document was successfully uploaded to BaseX
                # Update object to reference ID in BaseX
                instance.basex_docid = basex_id
                instance.save()

# this method is called before an object is deleted
@receiver(pre_delete, sender=Article)
def delete_basex_document(sender, instance, **kwargs):
    # the object had a document
    if instance.document:
        if os.path.isfile(instance.document.path):
            # remove the file
            os.remove(instance.document.path)

        # URL to delete the document
        rest_url = Constants.BASEX_REST_URL + '/' + Constants.BASEX_DB \
            + '/' + instance.basex_docid
        print('Calling DELETE ' + rest_url)
        r = requests.delete(rest_url,
            auth=Constants.BASEX_CREDENTIALS,
        )
        print(str(r.status_code) + ' ' + r.text)
