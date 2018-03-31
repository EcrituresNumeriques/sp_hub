from django.conf.urls import url, include

from .views.conversation import ConversationList, ConversationAdd, ConversationEdit, ConversationDetail

app_name = 'sp_app'

conversation_patterns = [
    url(r'^$', ConversationList.as_view(), name='list_conversations'),
    url(r'^new$', ConversationAdd.as_view(), name='add_conversation'),
    url(r'^(?P<pk>.+)/$', ConversationDetail.as_view(), name='display_conversation'),
#    url(r'^(?P<pk>.+)/edit$', add_change_spkeyword, name='change_conversation'),
    url(r'^(?P<pk>.+)/edit$', ConversationEdit.as_view(), name='change_conversation'),
]

urlpatterns = [
    url(r'^conversations/', include(conversation_patterns)),
]
