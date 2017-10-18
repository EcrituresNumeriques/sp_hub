from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_app.models import Article, SPKeyword
from sp_app.forms import SPKeywordForm
from sp_app.sp_keywords import import_from_csv

import json

class SPKeywordList(ListView):
    model = SPKeyword
    context_object_name = 'keywords'
    template_name = 'sp_keywords/list_page.html'


class SPKeywordDisplay(DetailView):
    model = SPKeyword
    context_object_name = 'keyword'
    template_name = 'sp_keywords/display.html'

    def get_context_data(self, **kwargs):
        context = super(SPKeywordDisplay, self).get_context_data(**kwargs)
        context['tagged_articles'] = Article.objects.filter(keywords__id=1)
        return context


class SPKeywordEdit(UpdateView):
    model = SPKeyword
    fields = [ 'data' ]
    template_name = 'sp_keywords/edit.html'

    def get_success_url(self):
        return reverse('sp_app:display_sp_keyword', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super(SPKeywordEdit, self).form_valid(form)

def editor_tags_import(request):
    import_from_csv.my_import()
    return redirect('sp_app:list_sp_keywords')

class SPKeywordNew(CreateView):
    model = SPKeyword
    fields = [ 'data' ]
    template_name = 'sp_keywords/edit.html'

    def get_success_url(self):
        return reverse_lazy('sp_app:display_sp_keyword', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(SPKeywordNew, self).form_valid(form)
