from django.conf.urls import url, include

from .views.article import ArticleList, ArticleAdd, ArticleEdit, ArticleDetail, import_zip_file
from .views.keyword import KeywordList, KeywordAdd, KeywordEdit, KeywordDetail
from .views.category import CategoryList, CategoryAdd, CategoryEdit, CategoryDetail
from .views.conversation import ConversationList, ConversationAdd, ConversationEdit, ConversationDetail
app_name = 'sp_app'

article_patterns = [
    url(r'^$', ArticleList.as_view(), name='list_articles'),
    url(r'^new$', ArticleAdd.as_view(), name='add_article'),
    url(r'^zipimport$', import_zip_file, name='zipimport'),
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

conversation_patterns = [
    url(r'^$', ConversationList.as_view(), name='list_conversations'),
    url(r'^new$', ConversationAdd.as_view(), name='add_conversation'),
    url(r'^(?P<pk>.+)/$', ConversationDetail.as_view(), name='display_conversation'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_conversation'),
    url(r'^(?P<pk>.+)/edit$', ConversationEdit.as_view(), name='change_conversation'),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^keywords/', include(keyword_patterns)),
    url(r'^categories/', include(category_patterns)),
    url(r'^conversations/', include(conversation_patterns)),
]
