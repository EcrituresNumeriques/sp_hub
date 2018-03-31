from django import forms

from .models import SPKeyword, SPCategory

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
