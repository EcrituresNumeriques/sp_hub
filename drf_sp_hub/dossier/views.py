from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Dossier
from .forms import DossierForm

from lxml import etree

class DossierList(ListView):
    model = Dossier
    context_object_name = 'dossiers'
    template_name = 'list_page.html'

class DossierDetail(DetailView):
    model = Dossier
    template_name = 'display.html'

class DossierEdit(UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'edit.html'

class DossierAdd(CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'edit.html'
