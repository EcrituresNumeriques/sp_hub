from django import forms

from .models import Dossier

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        fields = [ 'title', 'redacteurs', 'articles' ]
