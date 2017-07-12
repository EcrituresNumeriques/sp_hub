from django.conf.urls import url

from . import views

app_name = 'sp_app'

urlpatterns = [
    url(r'^list/$', views.list_articles, name='list_articles'),
    url(r'^display/(?P<docid>.+)/$', views.display, name='display'),

]
