from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Article
from .forms import ArticleForm

from lxml import etree

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
