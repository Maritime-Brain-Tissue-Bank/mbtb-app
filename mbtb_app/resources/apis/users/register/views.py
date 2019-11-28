from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer
from .permissions import IsAuthenticated, IsPostAllowed


# For authenticating admin credentials and return auth token
class NewUsersListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.filter(pending_approval='Y')  # filtering to fetch only pending requests
    serializer_class = UsersSerializer


# For new user registration requests and only post request allowed
class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostAllowed]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
