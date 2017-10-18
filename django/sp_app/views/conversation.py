from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from sp_app.models import Conversation
from sp_app.forms import ConversationForm


class ConversationList(ListView):
    model = Conversation
    context_object_name = 'conversations'
    template_name = 'conversations/list_page.html'


class ConversationDisplay(DetailView):
    model = Conversation
    context_object_name = 'conversation'
    template_name = 'conversations/display.html'


class ConversationEdit(UpdateView):
    model = Conversation
    fields = [ 'title', 'articles', 'timeline', 'keywords' ]
    template_name = 'conversations/edit.html'

    def get_success_url(self):
        return reverse('sp_app:display_conversation', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.has_perm('sp_app.change_conversation'):
            return super(ConversationEdit, self).form_valid(form)
        else:
            return HttpResponseForbidden()

# Class based view, form
class ConversationNew(CreateView):
    model = Conversation
    fields = [ 'title', 'articles', 'keywords', 'timeline', 'references' ]
    template_name = 'conversations/edit.html'

    def get_success_url(self):
        return reverse_lazy('sp_app:display_conversation', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.has_perm('sp_app.add_conversation'):
            form.instance.creator = self.request.user
            return super(ConversationNew, self).form_valid(form)
        else:
            return HttpResponseForbidden()
