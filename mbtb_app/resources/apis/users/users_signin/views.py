from django.http import HttpResponse
from rest_framework import views, response
from rest_framework.permissions import AllowAny
from .models import UsersAccount
import jwt


class UsersAccountView(views.APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        if not request.data:
            return response.Response({'Error': "Please provide username/password"}, status="400")

        email = request.data['email']
        password_hash = request.data['password']

        try:
            user = UsersAccount.objects.get(email=email, password_hash=password_hash)
        except UsersAccount.DoesNotExist:
            return response.Response({'Error': "Invalid username/password"}, status="400")

        if user:
            payload = {
                'id': user.id,
                'email': user.email,
                'password_hash': user.password_hash
            }
            jwt_token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')

            return HttpResponse(
                jwt_token,
                status=200,
                content_type="application/json"
            )
