from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Conversation


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Article
        fields = ('id', 'title', 'created_by', 'created_on')

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'created_by', 'created_on', 'updated_on', 'timeline')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='article-detail')
    conversations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='conversation-detail')
    class Meta:
        model = User
        fields = ('id', 'username', 'articles', 'conversations')
