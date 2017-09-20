from django.forms import ModelForm
from .models import Article, Conversation, EditorTag

class ConversationForm(ModelForm):
    class Meta:
        model = Conversation
        fields = [ 'title', 'articles', ]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'document', ]

class EditorTagForm(ModelForm):
    class Meta:
        model = EditorTag
        fields = [ 'description', ]
