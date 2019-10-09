from django.http import HttpResponse
from rest_framework import views, viewsets, response
from .models import AdminAccount, Users
from .serializers import UsersSerializer
from .permissions import IsAuthenticated, IsPostAllowed
import jwt
import datetime


class AdminAccountView(views.APIView):

    def post(self, request):
        if not request.data:
            return response.Response({'Error': "Please provide username/password"}, status="400")

        email = request.data['email']
        password_hash = request.data['password']

        try:
            admin = AdminAccount.objects.get(email=email, password_hash=password_hash)
        except AdminAccount.DoesNotExist:
            return response.Response({'Error': "Invalid username/password"}, status="400")

        if admin:
            payload = {
                'id': admin.id,
                'email': admin.email,
            }
            jwt_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')

            return HttpResponse(
                jwt_token,
                status=200,
                content_type="application/json"
            )


class NewUsersListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.filter(pending_approval='Y')
    serializer_class = UsersSerializer


class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostAllowed]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
