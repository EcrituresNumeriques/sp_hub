from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import list_route

from django.contrib.auth.models import User

from sp_app.models import Article, Conversation, SPKeyword, SPCategory
from .serializers import ArticleSerializer, ConversationSerializer
from .serializers import SPKeywordSerializer, SPCategorySerializer
from .serializers import UserSerializer

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
    def editor(self, request):
        queryset = SPKeyword.objects.filter(aligned=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def author(self, request):
        queryset = SPKeyword.objects.filter(aligned=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
