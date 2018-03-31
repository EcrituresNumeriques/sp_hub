from django.conf.urls import url, include

from .views import DossierList, DossierAdd, DossierDetail, DossierEdit

app_name = 'dossier'

dossier_patterns = [
    url(r'^$', DossierList.as_view(), name='list'),
    url(r'^new$', DossierAdd.as_view(), name='add'),
    url(r'^(?P<pk>.+)/$', DossierDetail.as_view(), name='display'),
    url(r'^(?P<pk>.+)/edit$', DossierEdit.as_view(), name='edit'),
]

urlpatterns = [
    url(r'^dossiers/', include(dossier_patterns)),
]
