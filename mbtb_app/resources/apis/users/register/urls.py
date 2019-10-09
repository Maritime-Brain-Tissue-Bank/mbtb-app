from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list_new_users', views.NewUsersListViewSet)
router.register('add_new_users', views.NewUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
