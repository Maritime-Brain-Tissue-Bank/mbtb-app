from django.http import HttpResponse
from rest_framework import views, response, viewsets
from .models import Users
from .serializers import UsersSerializer
from resources.permissions.is_post_allowed import IsPostAllowed
import jwt


# This view authenticate users and return auth_token, allowed request: post only
class UsersAccountView(views.APIView):
    permission_classes = [IsPostAllowed, ]

    def post(self, request):
        if not request.data:
            return response.Response({'Error': "Please provide username/password"}, status="400")

        email = request.data['email']
        password_hash = request.data['password']

        user = Users.objects.filter(email=email, password_hash=password_hash)
        if not user:
            return response.Response({'Error': "Invalid username/password"}, status="400")

        elif user[0].suspend is 'Y':
            return response.Response({'Error': 'Your account is suspended. Please contact admin.'}, status="400")

        else:
            payload = {
                'id': user[0].id,
                'email': user[0].email,
                'password_hash': user[0].password_hash
            }
            jwt_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')

            return HttpResponse(
                jwt_token,
                status=200,
                content_type="application/json"
            )


# For new user registration requests and only post request allowed
class NewUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPostAllowed]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
