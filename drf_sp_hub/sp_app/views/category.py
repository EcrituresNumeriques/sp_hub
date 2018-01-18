from sp_app.models import SPCategory
from sp_app.forms import SPCategoryForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView

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
