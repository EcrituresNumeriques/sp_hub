import logging
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.core.files import File
import os

from django.contrib.auth.models import User
from .serializers import UserSerializer

from .models import Article, Conversation, SPKeyword, SPCategory
from .serializers import ArticleSerializer, ConversationSerializer
from .serializers import SPKeywordSerializer, SPCategorySerializer

logger = logging.getLogger(__name__)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    @list_route()
    def import_bulk(self, request):
        Article.objects.all().delete()
        SPKeyword.objects.all().delete()
        my_files = []
        for f in os.listdir('resources/html'):
            if f.startswith('SP') and f.endswith('.html'):
                my_files.append(f)
                fp = open(os.path.join('resources/html', f), 'rb')
                logger.info('Bulk import: ' + f)
                a = Article.objects.create(title=f)
                a.html_file.save(f, File(fp))

        return Response(','.join(my_files))

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
