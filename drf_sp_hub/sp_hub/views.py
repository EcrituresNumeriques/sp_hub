import logging

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_api.models import Article, SPKeyword

logger = logging.getLogger(__name__)

def homepage_view(request):
    return render(request, 'frontend/index.html')

class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/list_page.html'

class KeywordsList(ListView):
    model = SPKeyword
    context_object_name = 'keywords'
    template_name = 'keywords/list_page.html'

def display_article(request, pk):
    article = Article.objects.get(pk=pk)

    if article.html_file:
        data = article.html_file.read()

    return render(request, 'articles/display.html', {
        'article': article,
        'basex_document': data.decode(),
        'annotations': [],
        'conversations': article.conversations.all(),
        'keywords': article.keywords.all(),
    })

def display_keyword(request, pk):
    keyword = SPKeyword.objects.get(pk=pk)
    logger.info(keyword.articles)
    return render(request, 'keywords/display.html', {
        'keyword': keyword,
        'articles': keyword.articles.all(),
    })
