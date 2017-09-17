from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Article
from .forms import ArticleForm
from .sp_constants import Constants

import requests
import json

def new_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            return redirect('sp_app:display', docid=article.pk)
    else:
        form = ArticleForm()
        return render(request, 'articles/edit.html', { 'form': form })

def display(request, docid):
    article = Article.objects.get(pk=docid)

    basex_id = str(article.pk) + '.html'
    data = ''

    my_url = Constants.BASEX_URL + '/sph/tim' +  "/articles/view/" + basex_id
    print('Calling ' + my_url)
    r_basex = requests.get(my_url)

    if r_basex.status_code == 200:
        data = r_basex.content

    """ Look for annotations in hypothes.is """
    my_url = Constants.HYPOTHESIS_API_URL + "/search?uri=" + request.build_absolute_uri()
    r_hypothesis = requests.get(my_url)

    if r_hypothesis.status_code == 200:
        annotations = json.loads(r_hypothesis.content)

    return render(request, 'articles/display.html', {
        'django_article': article,
        'article': data,
        'annotations': annotations['rows'],
    })


def list_articles(request):
    articles = Article.objects.all()

    return render(request, 'articles/list.html', { 'articles': articles, })

def list_articles_basex(request):
    my_url = Constants.BASEX_API_URL + "/articles/list"
    r = requests.get(my_url)

    if r.status_code == 200:
        data = json.loads(r.content)

    return render(request, 'articles/list_basex.html', { 'articles': data, 'source_url': my_url})
