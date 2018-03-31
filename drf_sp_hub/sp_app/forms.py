from django import forms

from .models import Conversation

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = [ 'title', 'articles', 'keywords',  ]
        hidden_fields = [ 'timeline', ]
        widgets = {
            'articles': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'}),
            'keywords': forms.SelectMultiple(attrs={'class': 'select-multi-keywords, form-control'})
        }
