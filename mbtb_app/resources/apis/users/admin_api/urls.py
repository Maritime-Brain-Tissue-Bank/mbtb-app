from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list_new_users', views.NewUsersViewSet)
router.register('current_users', views.CurrentUsersViewSet)
router.register('suspended_users', views.SuspendedUsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin_auth', views.AdminAccountGetTokenView.as_view())
]
