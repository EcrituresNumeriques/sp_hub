from django.conf.urls import include, url
from . import views

app_name = 'sp_app'

article_patterns = [
    url(r'^$', views.ArticleList.as_view(), name='list_articles'),
    url(r'^new$', views.new_article, name='new_article'),
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
    url(r'^(?P<pk>.+)/$', views.EditorTagDisplay.as_view(), name='display_editor_tag'),
    url(r'^(?P<pk>.+)/edit$', views.EditorTagEdit.as_view(), name='edit_editor_tag'),
]

user_tag_patterns = [
    url(r'^$', views.UserTagList.as_view(), name='list_user_tags'),
    url(r'^(?P<pk>.+)/$', views.UserTagDisplay.as_view(), name='display_user_tag'),
    url(r'^(?P<pk>.+)/edit$', views.UserTagEdit.as_view(), name='edit_user_tag'),
]

tag_patterns = [
    url(r'^editor/', include(editor_tag_patterns)),
    url(r'^user/', include(user_tag_patterns)),
]

urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^conversations/', include(conversation_patterns)),
    url(r'^tags/', include(tag_patterns)),
]
