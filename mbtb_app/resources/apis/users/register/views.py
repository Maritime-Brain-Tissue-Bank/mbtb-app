from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer
from permissions.is_post_allowed import IsPostAllowed


# For new user registration requests and only post request allowed
class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostAllowed]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
