from django.conf.urls import url

from . import views

app_name = 'sp_app'

urlpatterns = [
    url(r'^view/(?P<docid>.+)/$', views.display, name='display'),
    url(r'^(?P<action>.+)/$', views.list_titles, name='list_titles'),

]
