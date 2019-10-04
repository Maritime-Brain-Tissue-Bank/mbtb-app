from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer
from .permissions import IsAuthenticated, IsPostAllowed


class NewUsersListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.filter(pending_approval='Y')
    serializer_class = UsersSerializer


class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostAllowed]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
