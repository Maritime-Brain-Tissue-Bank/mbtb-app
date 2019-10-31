from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('brain_dataset', views.BrainDatasetAPIView)
router.register('other_details', views.DatasetOthrDetailsAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
