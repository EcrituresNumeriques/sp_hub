from .models import SPKeyword, SPCategory
from .forms import SPKeywordForm, SPCategoryForm

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

class CategoryList(ListView):
    model = SPCategory
    context_object_name = 'categories'
    template_name = 'categories/list_page.html'

class CategoryDetail(DetailView):
    model = SPCategory
    context_object_name = 'category'
    template_name = 'categories/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keywords = self.object.keywords.all()
        articles = []
        context['keywords'] = keywords
        for kw in keywords:
            articles.extend(kw.articles.all())
        context['articles'] = articles
        return context

class CategoryEdit(UpdateView):
    model = SPCategory
    form_class = SPCategoryForm
    template_name = 'categories/edit.html'

class CategoryAdd(CreateView):
    model = SPCategory
    form_class = SPCategoryForm
    template_name = 'categories/edit.html'
