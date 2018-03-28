from sp_app.models import Article
from sp_app.forms import ArticleForm

from lxml import etree

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django import forms
from django.shortcuts import render
from sp_app.lib.zip_importer import ZipImporter

class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/list_page.html'

class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.html_file:
            # Init HTML parser
            parser = etree.HTMLParser()
            tree = etree.parse(self.object.html_file, parser)

            extra_head = tree.xpath("//head/meta")
            context['extra_head'] = ''
            for elm in extra_head:
                context['extra_head'] += etree.tostring(elm).decode()

            body_elem = tree.xpath("//body/div[@class='article']")
            if(body_elem):
                context['html_document'] = etree.tostring(body_elem[0]).decode()
            else:
                context['html_document'] = 'No content'
        return context

class ArticleEdit(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'

class ArticleAdd(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'

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
