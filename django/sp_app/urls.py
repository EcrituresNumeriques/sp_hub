from django.conf.urls import include, url
from . import views

app_name = 'sp_app'

article_patterns = [
    url(r'^(?P<docid>.+)/$', views.display_article, name='display_article'),
    url(r'^new$', views.new_article, name='new_article'),
]

conversation_patterns = [
    url(r'^$', views.ConversationList.as_view(), name='list_conversations'),
    url(r'^(?P<pk>.+)/$', views.ConversationDisplay.as_view(), name='display_conversation'),
    url(r'^new/$', views.ConversationFormView.as_view(), name='new_conversation'),
]
urlpatterns = [
    url(r'^articles/', include(article_patterns)),
    url(r'^conversations/', include(conversation_patterns)),
]
