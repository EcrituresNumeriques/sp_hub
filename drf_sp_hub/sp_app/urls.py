from django.conf.urls import url, include

from .views.article import ArticleList, ArticleAdd, ArticleEdit, ArticleDetail
from .views.keyword import KeywordList, KeywordAdd, KeywordEdit, KeywordDetail
from .views.category import CategoryList, CategoryAdd, CategoryEdit, CategoryDetail
app_name = 'sp_app'

article_patterns = [
    url(r'^$', ArticleList.as_view(), name='list_articles'),
    url(r'^new$', ArticleAdd.as_view(), name='add_article'),
    url(r'^(?P<pk>.+)/$', ArticleDetail.as_view(), name='display_article'),
    url(r'^(?P<pk>.+)/edit$', ArticleEdit.as_view(), name='change_article'),
]

keyword_patterns = [
    url(r'^$', KeywordList.as_view(), name='list_keywords'),
    url(r'^new$', KeywordAdd.as_view(), name='add_keyword'),
    url(r'^(?P<pk>.+)/$', KeywordDetail.as_view(), name='display_keyword'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_keyword'),
    url(r'^(?P<pk>.+)/edit$', KeywordEdit.as_view(), name='change_keyword'),
]

category_patterns = [
    url(r'^$', CategoryList.as_view(), name='list_categories'),
    url(r'^new$', CategoryAdd.as_view(), name='add_category'),
    url(r'^(?P<pk>.+)/$', CategoryDetail.as_view(), name='display_category'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_category'),
    url(r'^(?P<pk>.+)/edit$', CategoryEdit.as_view(), name='change_category'),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^keywords/', include(keyword_patterns)),
    url(r'^categories/', include(category_patterns)),
]
