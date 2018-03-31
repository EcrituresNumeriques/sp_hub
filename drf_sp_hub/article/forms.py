from django import forms
from datetimewidget.widgets import DateTimeWidget

from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [ 'title', 'html_file', 'pdf_file', 'keywords', 'type_article', 'published_on', 'published' ]
        widgets = {
            'keywords': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'}),
            'published_on': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True),
        }
