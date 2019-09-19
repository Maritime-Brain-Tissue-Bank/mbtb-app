from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('new_user', views.NewUsersViewSet)

urlpatterns = [
    path('', include(router.urls))
]