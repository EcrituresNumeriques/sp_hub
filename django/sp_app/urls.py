from django.conf.urls import include, url
from . import views

app_name = 'sp_app'

article_patterns = [
    url(r'^$', views.ArticleList.as_view(), name='list_articles'),
    url(r'^new/$', views.ArticleNew.as_view(), name='new_article'),
    url(r'^(?P<pk>.+)/$', views.display_article, name='display_article'),
    url(r'^(?P<pk>.+)/edit$', views.ArticleEdit.as_view(), name='edit_article'),

]

conversation_patterns = [
    url(r'^$', views.ConversationList.as_view(), name='list_conversations'),
    url(r'^new/$', views.ConversationNew.as_view(), name='new_conversation'),
    url(r'^(?P<pk>.+)/$', views.ConversationDisplay.as_view(), name='display_conversation'),
    url(r'^(?P<pk>.+)/edit$', views.ConversationEdit.as_view(), name='edit_conversation'),
]

sp_keywords_patterns = [
    url(r'^$', views.SPKeywordList.as_view(), name='list_sp_keywords'),
    url(r'new/$', views.SPKeywordNew.as_view(), name='new_sp_keyword'),
    url(r'^(?P<pk>.+)/$', views.SPKeywordDisplay.as_view(), name='display_sp_keyword'),
    url(r'^(?P<pk>.+)/edit$', views.SPKeywordEdit.as_view(), name='edit_sp_keyword'),
]

tag_patterns = [
    url(r'^import/$', views.editor_tags_import),
    url(r'^', include(sp_keywords_patterns)),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^conversations/', include(conversation_patterns)),
    url(r'^keywords/', include(sp_keywords_patterns)),
]
