from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Conversation, SPKeyword


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    keywords = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='spkeyword-detail')
    class Meta:
        model = Article
        fields = ('id', 'title', 'created_by', 'created_on', 'url', 'html_file', 'keywords')

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'created_by', 'created_on', 'updated_on', 'description', 'timeline')

class SPKeywordSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='article-detail')
    parent_category = serializers.HyperlinkedRelatedField(read_only=True, view_name='spkeyword-detail')
    children = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='spkeyword-detail')
    #children = serializers.StringRelatedField()
    class Meta:
        model = SPKeyword
        fields = ('id', 'name', 'url', 'aligned', 'parent_category', 'data', 'articles', 'children')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='article-detail')
    conversations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='conversation-detail')
    class Meta:
        model = User
        fields = ('id', 'username', 'articles', 'conversations')
