from rest_framework import viewsets
from .models import NewUsers
from .serializers import NewUsersSerializer


class NewUsersViewSet(viewsets.ModelViewSet):
    queryset = NewUsers.objects.all()
    serializer_class = NewUsersSerializer
