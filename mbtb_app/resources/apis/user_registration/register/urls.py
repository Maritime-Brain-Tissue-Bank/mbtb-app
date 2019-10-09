from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list_new_users', views.NewUsersListViewSet)
router.register('new_users', views.NewUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin_auth', views.AdminAccountView.as_view())
]
