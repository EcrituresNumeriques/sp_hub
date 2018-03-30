from django import forms
from datetimewidget.widgets import DateTimeWidget

from .models import Article, Conversation, SPKeyword, SPCategory

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'html_file', 'pdf_file', 'keywords', 'type_article', 'published_on', 'published' ]
        widgets = {
            'keywords': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'}),
            'published_on': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True),
        }

class SPKeywordForm(forms.ModelForm):
    class Meta:
        model = SPKeyword
        fields = [ 'name', 'language', 'data', 'aligned', 'is_editor', 'is_translation']
        hidden_fields = [ 'data' ]
        widgets = {
            'is_translation': forms.Select(attrs={'class': 'select-multi-keywords, form-control'})
        }

class SPCategoryForm(forms.ModelForm):
    class Meta:
        model = SPCategory
        fields = [ 'name' ]

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = [ 'title', 'articles', 'keywords',  ]
        hidden_fields = [ 'timeline', ]
        widgets = {
            'articles': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'}),
            'keywords': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'})
        }
