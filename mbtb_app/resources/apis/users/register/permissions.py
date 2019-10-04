from rest_framework import exceptions, permissions
from rest_framework.authentication import get_authorization_header
from django.http import HttpResponse
from admin_signin.models import AdminAccount
import jwt


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # only allow admin's GET request via authorized token
        if request.method == 'GET':
            admin = self.authenticate(request)
            return admin

        if request.method == 'PATCH':
            return True

        return False

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        payload = jwt.decode(token, "SECRET_KEY")
        email = payload['email']
        userid = payload['id']
        try:
            admin = AdminAccount.objects.get(id=userid, email=email)
            return True
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")
        except AdminAccount.DoesNotExist:
            return False

    def authenticate_header(self, request):
        return 'Token'


class IsPostAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests, no authentication
        if request.method == 'POST':
            return True

        return False
