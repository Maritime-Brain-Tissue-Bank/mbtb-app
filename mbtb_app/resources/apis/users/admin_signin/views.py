from django.http import HttpResponse
from rest_framework import views, response
from rest_framework.permissions import AllowAny
from .models import AdminAccount
import jwt


# Authenticate credentials for admin and return auth token
# Also, written view for post request only
class AdminAccountView(views.APIView):
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
