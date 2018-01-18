from django import forms
from .models import Article, Conversation, SPKeyword

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'html_file', 'keywords' ]
        widgets = {
            'keywords': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'})
        }

class SPKeywordForm(forms.ModelForm):
    class Meta:
        model = SPKeyword
        fields = [ 'name', 'data', 'aligned', 'is_editor']
        hidden_fields = [ 'data' ]
