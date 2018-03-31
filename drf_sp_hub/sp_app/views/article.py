from sp_app.models import Article
from sp_app.forms import ArticleForm

from lxml import etree

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django import forms
from django.shortcuts import render
from sp_app.utils.zip_importer import ZipImporter

class ZipImportForm(forms.Form):
    zip_file = forms.FileField()

def import_zip_file(request):
    if request.method == 'POST':
        # Do something
        form = ZipImportForm(request.POST, request.FILES)
        if form.is_valid():
            zipimport = ZipImporter(request.FILES['zip_file'])
            form_msg = zipimport.process_files()
            zipimport.clean_files()
    else:
        form = ZipImportForm()
        form_msg = 'upload file'

    return render(request, 'articles/zipimport.html', { 'form': form, 'form_msg': form_msg })
