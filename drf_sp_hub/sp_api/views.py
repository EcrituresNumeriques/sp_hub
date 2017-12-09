from django.shortcuts import render
from rest_framework import viewsets, generics

from django.contrib.auth.models import User
from .serializers import UserSerializer

from .models import Article, Conversation, SPKeyword
from .serializers import ArticleSerializer, ConversationSerializer, SPKeywordSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class SPKeywordViewSet(viewsets.ModelViewSet):
    queryset = SPKeyword.objects.all()
    serializer_class = SPKeywordSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
