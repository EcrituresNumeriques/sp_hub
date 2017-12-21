from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from sp_api import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'conversations', views.ConversationViewSet)
router.register(r'keywords', views.SPKeywordViewSet)
router.register(r'categories', views.SPCategoryViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
