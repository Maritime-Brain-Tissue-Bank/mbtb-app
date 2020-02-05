from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('add_new_tissue_requests', views.PostNewTissueRequestsAPIView)
router.register('get_new_tissue_requests', views.GetNewTissueRequestsAPIView)
router.register('get_archive_tissue_requests', views.GetArchiveTissueRequestsAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
