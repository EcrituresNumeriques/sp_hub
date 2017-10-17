from django.forms import ModelForm
from .models import Article, Conversation, SPKeyword

class ConversationForm(ModelForm):
    class Meta:
        model = Conversation
        fields = [ 'title', 'articles', ]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'document', ]

class SPKeywordForm(ModelForm):
    class Meta:
        model = SPKeyword
        fields = [ 'description', ]
