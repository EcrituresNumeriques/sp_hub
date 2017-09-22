from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_app.models import EditorTag
from sp_app.forms import EditorTagForm
from sp_app.sp_keywords import import_from_csv

import json

class EditorTagList(ListView):
    model = EditorTag
    context_object_name = 'tags'
    template_name = 'tags/editor_list_page.html'


class EditorTagDisplay(DetailView):
    model = EditorTag
    context_object_name = 'tag'
    template_name = 'tags/editor_display.html'


class EditorTagEdit(UpdateView):
    model = EditorTag
    fields = [ 'description', 'link_rameau', 'categorie' ]
    template_name = 'tags/edit.html'

    def get_success_url(self):
        return reverse('sp_app:display_editor_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super(EditorTagEdit, self).form_valid(form)

def editor_tags_import(request):
    import_from_csv.my_import()
    return redirect('sp_app:list_editor_tags')

class EditorTagNew(CreateView):
    model = EditorTag
    fields = [ 'name', 'description', 'link_rameau', 'categorie' ]
    template_name = 'tags/edit.html'

    def get_success_url(self):
        return reverse_lazy('sp_app:display_editor_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(EditorTagNew, self).form_valid(form)
