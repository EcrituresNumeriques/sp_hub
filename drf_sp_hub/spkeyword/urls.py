from django.conf.urls import url, include

from .views import KeywordList, KeywordAdd, KeywordEdit, KeywordDetail
from .views import CategoryList, CategoryAdd, CategoryEdit, CategoryDetail

app_name = 'spkeyword'

keyword_patterns = [
    url(r'^$', KeywordList.as_view(), name='list'),
    url(r'^new$', KeywordAdd.as_view(), name='add'),
    url(r'^(?P<pk>.+)/$', KeywordDetail.as_view(), name='display'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_keyword'),
    url(r'^(?P<pk>.+)/edit$', KeywordEdit.as_view(), name='edit'),
]

category_patterns = [
    url(r'^$', CategoryList.as_view(), name='list_categories'),
    url(r'^new$', CategoryAdd.as_view(), name='add_category'),
    url(r'^(?P<pk>.+)/$', CategoryDetail.as_view(), name='display_category'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_category'),
    url(r'^(?P<pk>.+)/edit$', CategoryEdit.as_view(), name='edit_category'),
]

urlpatterns = [
    url(r'^keywords/', include(keyword_patterns)),
    url(r'^categories/', include(category_patterns)),
]
