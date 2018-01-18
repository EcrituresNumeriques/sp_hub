import logging
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.core.files import File
import os

from .forms import ArticleForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView

from django.contrib.auth.models import User
from .serializers import UserSerializer

from .models import Article, Conversation, SPKeyword, SPCategory
from .serializers import ArticleSerializer, ConversationSerializer
from .serializers import SPKeywordSerializer, SPCategorySerializer

logger = logging.getLogger(__name__)

class ArticleEdit(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'

class ArticleAdd(CreateView):
    model = Article
    fields = [ 'title', 'html_file' ]
    template_name = 'keywords/edit.html'

class SPKeywordEdit(UpdateView):
    model = SPKeyword
    fields = [ 'name', 'data' ]
    template_name = 'keywords/edit.html'

class SPKeywordAdd(CreateView):
    model = SPKeyword
    fields = [ 'name', 'data' ]
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
