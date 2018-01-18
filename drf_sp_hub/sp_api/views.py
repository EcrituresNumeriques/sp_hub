import logging
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.core.files import File
import os
from lxml import etree

from .forms import ArticleForm, SPKeywordForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.models import User
from .serializers import UserSerializer

from .models import Article, Conversation, SPKeyword, SPCategory
from .serializers import ArticleSerializer, ConversationSerializer
from .serializers import SPKeywordSerializer, SPCategorySerializer

logger = logging.getLogger(__name__)

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
            body_elem = tree.xpath("//body")
            body_html = etree.tostring(body_elem[0])
            context['basex_document'] = body_html.decode()

        context['keywords'] = self.object.keywords.all()
        return context

class ArticleEdit(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'

class ArticleAdd(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/edit.html'

class SPKeywordList(ListView):
    model = SPKeyword
    context_object_name = 'keywords'
    template_name = 'keywords/list_page.html'

class SPKeywordDetail(DetailView):
    model = SPKeyword
    context_object_name = 'keyword'
    template_name = 'keywords/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.object.articles.all()
        return context

class SPKeywordEdit(UpdateView):
    model = SPKeyword
    form_class = SPKeywordForm
    template_name = 'keywords/edit.html'

class SPKeywordAdd(CreateView):
    model = SPKeyword
    form_class = SPKeywordForm
    template_name = 'keywords/edit.html'

"""
THESE ARE THE API VIEWS (DRF)
"""
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class SPCategoryViewSet(viewsets.ModelViewSet):
    queryset = SPCategory.objects.all()
    serializer_class = SPCategorySerializer

class SPKeywordViewSet(viewsets.ModelViewSet):
    queryset = SPKeyword.objects.all()
    serializer_class = SPKeywordSerializer

    @list_route()
    def list_editor(self, request):
        queryset = SPKeyword.objects.filter(aligned=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def list_author(self, request):
        queryset = SPKeyword.objects.filter(aligned=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
