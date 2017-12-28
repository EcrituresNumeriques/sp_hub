from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Conversation, SPKeyword, SPCategory


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(view_name='sp_api:article-detail')
    keywords = serializers.StringRelatedField(many=True, read_only=True)
    keywords_url = serializers.HyperlinkedRelatedField(
        source='keywords',
        many=True, read_only=True, view_name='sp_api:spkeyword-detail'
    )
    class Meta:
        model = Article
        fields = ('id', 'title', 'created_by', 'created_on', 'url', 'html_file', 'keywords', 'keywords_url')

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Conversation
        fields = ('id', 'title', 'created_by', 'created_on', 'updated_on', 'description', 'timeline')

class SPCategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='sp_api:spcategory-detail')
    keywords = serializers.StringRelatedField(many=True)
    keywords_url = serializers.HyperlinkedRelatedField(
        source='keywords',
        many=True, read_only=True, view_name='sp_api:spkeyword-detail'
    )
    class Meta:
        model = SPCategory
        fields = ('id', 'name', 'url', 'keywords', 'keywords_url')

class SPKeywordSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='sp_api:article-detail')
    url = serializers.HyperlinkedIdentityField(view_name='sp_api:spkeyword-detail')
    category = serializers.StringRelatedField()
    category_url = serializers.HyperlinkedRelatedField(
        source='category',
        read_only=True, view_name='sp_api:spcategory-detail'
    )
    class Meta:
        model = SPKeyword
        fields = ('id', 'name', 'url', 'aligned', 'category_url', 'category', 'data', 'articles')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='display_article')
    conversations = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='conversation-detail')
    class Meta:
        model = User
        fields = ('id', 'username', 'articles', 'conversations')
