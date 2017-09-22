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

editor_tag_patterns = [
    url(r'^$', views.EditorTagList.as_view(), name='list_editor_tags'),
    url(r'new/$', views.EditorTagNew.as_view(), name='new_editor_tag'),
    url(r'^(?P<pk>.+)/$', views.EditorTagDisplay.as_view(), name='display_editor_tag'),
    url(r'^(?P<pk>.+)/edit$', views.EditorTagEdit.as_view(), name='edit_editor_tag'),
]

tag_patterns = [
    url(r'^editor/', include(editor_tag_patterns)),
    url(r'^import/$', views.editor_tags_import),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^conversations/', include(conversation_patterns)),
    url(r'^tags/', include(tag_patterns)),
]
