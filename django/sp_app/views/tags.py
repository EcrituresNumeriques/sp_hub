from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_app.models import EditorTag, UserTag
from sp_app.forms import EditorTagForm, UserTagForm


class EditorTagList(ListView):
    model = EditorTag
    context_object_name = 'tags'
    template_name = 'tags/user_list_page.html'


class EditorTagDisplay(DetailView):
    model = EditorTag
    context_object_name = 'tag'
    template_name = 'tags/user_display.html'


class EditorTagEdit(UpdateView):
    model = EditorTag
    fields = [ 'description' ]
    template_name = 'tags/edit.html'

    def get_success_url(self):
        return reverse('sp_app:display_user_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super(EditorTagEdit, self).form_valid(form)

# Class based view, form
class EditorTagNew(CreateView):
    model = EditorTag
    fields = [ 'description', 'articles' ]
    template_name = 'tags/user_new.html'

    def get_success_url(self):
        return reverse_lazy('sp_app:display_user_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(EditorTagNew, self).form_valid(form)

class UserTagList(ListView):
    model = UserTag
    context_object_name = 'tags'
    template_name = 'tags/user_list_page.html'


class UserTagDisplay(DetailView):
    model = UserTag
    context_object_name = 'tag'
    template_name = 'tags/user_display.html'


class UserTagEdit(UpdateView):
    model = UserTag
    fields = [ 'description' ]
    template_name = 'tags/edit.html'

    def get_success_url(self):
        return reverse('sp_app:display_user_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super(UserTagEdit, self).form_valid(form)

# Class based view, form
class UserTagNew(CreateView):
    model = UserTag
    fields = [ 'description', 'articles' ]
    template_name = 'tags/user_new.html'

    def get_success_url(self):
        return reverse_lazy('sp_app:display_user_tag', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(UserTagNew, self).form_valid(form)
