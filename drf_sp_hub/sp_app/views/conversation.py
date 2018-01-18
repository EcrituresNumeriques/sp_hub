from sp_app.models import Conversation
from sp_app.forms import ConversationForm

import json

from django.views.generic import ListView, DetailView, CreateView, UpdateView

class ConversationList(ListView):
    model = Conversation
    context_object_name = 'conversations'
    template_name = 'conversations/list_page.html'

class ConversationDetail(DetailView):
    model = Conversation
    fields = [ 'title', 'timeline' ]
    template_name = 'conversations/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timeline'] = self.object.timeline
        return context

class ConversationEdit(UpdateView):
    model = Conversation
    form_class = ConversationForm
    template_name = 'conversations/edit.html'

class ConversationAdd(CreateView):
    model = Conversation
    form_class = ConversationForm
    template_name = 'conversations/edit.html'
