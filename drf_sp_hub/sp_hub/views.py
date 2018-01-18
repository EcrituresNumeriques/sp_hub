import logging
from lxml import etree

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_api.models import Article, SPKeyword

logger = logging.getLogger(__name__)

def homepage_view(request):
    return redirect('/articles/')
    #return render(request, 'frontend/index.html')
