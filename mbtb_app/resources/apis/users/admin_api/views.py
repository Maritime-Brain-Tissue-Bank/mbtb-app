from django.http import HttpResponse
from rest_framework import views, response, viewsets
from rest_framework.permissions import AllowAny
from .models import AdminAccount
from permissions.is_admin import IsAdmin
from register.models import Users
from register.serializers import UsersSerializer
import jwt


# Authenticate credentials for admin and return auth token
# Also, written view for post request only
class AdminAccountGetTokenView(views.APIView):
    permission_classes = [AllowAny, ]

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


# This view gets new registration requests and allow admin to approve their status.
class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Users.objects.filter(pending_approval='Y')  # filtering to fetch only pending requests
    serializer_class = UsersSerializer


# This view gets current users list and allow admin to suspend their account.
class CurrentUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    # filtering to fetch non-pending and active accounts
    queryset = Users.objects.filter(pending_approval='N', suspend='N')
    serializer_class = UsersSerializer


# This view gets suspended users list and allow admin to revert user's account status to normal.
class SuspendedUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    # filtering to fetch non-pending and suspended accounts
    queryset = Users.objects.filter(pending_approval='N', suspend='Y')
    serializer_class = UsersSerializer
