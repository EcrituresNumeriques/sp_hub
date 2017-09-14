from django.forms import ModelForm
from .models import Article, Conversation

class ConversationForm(ModelForm):
    class Meta:
        model = Conversation
        fields = [ 'title' ]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'document', ]
