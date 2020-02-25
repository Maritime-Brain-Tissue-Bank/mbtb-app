from rest_framework import viewsets
from .models import TissueRequests
from .serializers import TissueRequestsSerializer
from resources.permissions.is_authenticated import IsAuthenticated
from resources.permissions.is_admin import IsAdmin


# This class is to add a new tissue request, permission user only
class PostNewTissueRequestsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TissueRequests.objects.all()
    serializer_class = TissueRequestsSerializer


# This class is to fetch new tissue requests and confirm those requests, permission admin only
class GetNewTissueRequestsView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = TissueRequests.objects.filter(pending_approval='Y')  # filtering to fetch only pending requests
    serializer_class = TissueRequestsSerializer


# This class is to fetch archive tissue requests, permission admin only
class GetArchiveTissueRequestsView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = TissueRequests.objects.filter(pending_approval='N')  # filtering to fetch only archive requests
    serializer_class = TissueRequestsSerializer
