from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

# pass views to router as url
router.register('brain_dataset', views.PrimeDetailsAPIView)
router.register('other_details', views.OtherDetailsAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('add_new_data/', views.CreateDataAPIView.as_view()),
    path('get_select_options/', views.GetSelectOptions.as_view())
]
