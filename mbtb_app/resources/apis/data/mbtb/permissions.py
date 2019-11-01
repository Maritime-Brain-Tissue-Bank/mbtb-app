from rest_framework import exceptions, permissions
from rest_framework.authentication import get_authorization_header
from .models import AdminAccount, UserAccount
import jwt


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # only allow admin's GET request via authorized token
        if request.method == 'GET':
            admin = self.authenticate(request)
            return admin

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
        response = self.find_model(email, userid)
        return response

    # find request email from both models: admin, users
    def find_model(self, email, userid):
        models = [AdminAccount, UserAccount]
        response = []
        for Model in models:
            try:
                account = Model.objects.get(id=userid, email=email)
                response.append(True)
            except Model.DoesNotExist:
                response.append(False)
        if len(set(response)) == 2:
            return True

        return False

    def authenticate_header(self, request):
        return 'Token'
