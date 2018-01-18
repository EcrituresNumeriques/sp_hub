from sp_app.models import SPKeyword
from sp_app.forms import SPKeywordForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView

class KeywordList(ListView):
    model = SPKeyword
    context_object_name = 'keywords'
    template_name = 'keywords/list_page.html'

class KeywordDetail(DetailView):
    model = SPKeyword
    context_object_name = 'keyword'
    template_name = 'keywords/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.object.articles.all()
        return context

class KeywordEdit(UpdateView):
    model = SPKeyword
    form_class = SPKeywordForm
    template_name = 'keywords/edit.html'

class KeywordAdd(CreateView):
    model = SPKeyword
    form_class = SPKeywordForm
    template_name = 'keywords/edit.html'
