"""sp_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from .views import homepage_view
from .views import ArticleList, display_article
from .views import KeywordsList, display_keyword
from sp_api import views as spviews

app_name='sp_hub'

article_patterns = [
    url(r'^$', ArticleList.as_view(), name='list_articles'),
    url(r'^(?P<pk>.+)/$', display_article, name='display_article'),
]

keyword_patterns = [
    url(r'^$', KeywordsList.as_view(), name='list_keywords'),
    url(r'^(?P<pk>.+)/$', display_keyword, name='display_keyword'),
]

urlpatterns = [
    url(r'^api/', include('sp_api.urls', namespace='sp_api')),
    url(r'^admin/', admin.site.urls),
    url(r'^articles/', include(article_patterns)),
    url(r'^keywords/', include(keyword_patterns)),
    url(r'^/', homepage_view, name='home'),
]
