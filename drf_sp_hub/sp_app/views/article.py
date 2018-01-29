from sp_app.models import Article
from sp_app.forms import ArticleForm

from lxml import etree

from django.views.generic import ListView, DetailView, CreateView, UpdateView

class ArticleList(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'articles/list_page.html'

class ArticleDetail(DetailView):
    model = Article
    template_name = 'articles/display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basex_document'] = '<iframe style="width: 100%; height: -webkit-fill-available;" src="/static/articles/SP' + str(self.object.id_senspublic) + '.html"></iframe>'
        if self.object.html_file:
            pass
            # Init HTML parser
            # parser = etree.HTMLParser()
            # tree = etree.parse(self.object.html_file, parser)
            # body_elem = tree.xpath("//body")
            # body_html = etree.tostring(body_elem[0])
            # html_content = etree.tostring(tree.getroot())
            # context['basex_document'] = html_content.decode()

        return context

class ArticleEdit(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'

class ArticleAdd(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit.html'
