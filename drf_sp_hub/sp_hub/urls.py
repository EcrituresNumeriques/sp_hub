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

from django.contrib.auth import views as auth_views

from .views import homepage_view

app_name='sp_hub'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login,
        { 'template_name': 'core/login.html' },
        name='login'
    ),
    url(r'^logout/$', auth_views.logout, { 'next_page': '/' }, name='logout'),
    url(r'^api/', include('sp_api.urls', namespace='sp_api')),
    url(r'^', include('sp_app.urls', namespace='sp_app')),
    url(r'^$', homepage_view, name='home'),
]
