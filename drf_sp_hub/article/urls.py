from django.conf.urls import url, include

from .views import ArticleList, ArticleAdd, ArticleDetail, ArticleEdit

app_name = 'article'

article_patterns = [
    url(r'^$', ArticleList.as_view(), name='list'),
    url(r'^new$', ArticleAdd.as_view(), name='add'),
    url(r'^(?P<pk>.+)/$', ArticleDetail.as_view(), name='display'),
    url(r'^(?P<pk>.+)/edit$', ArticleEdit.as_view(), name='edit'),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
]
