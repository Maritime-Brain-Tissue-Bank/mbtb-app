from rest_framework import exceptions, permissions
from rest_framework.authentication import get_authorization_header
from .models import AdminAccount, UserAccount
import jwt


class IsAuthenticated(permissions.BasePermission):

    # Allow following request from user
    def has_permission(self, request, view):

        # only allow admin's GET request via authorized token
        if request.method == 'GET':
            valid_url = ['brain_dataset', 'other_details', 'get_select_options']

            # splitting url e.g. /brain_dataset/1/ to get brain_dataset for comparison
            url_path = request.path.split('/')
            if max(url_path) in valid_url:
                admin = self.authenticate(request)
                return admin

            # deny GET request if url is not in valid_url by default
            return False

        # only allow admin's POST request via authorized token
        if request.method == 'POST':
            valid_url = ['file_upload', 'add_new_data']

            # splitting url e.g. /brain_dataset/1/ to get brain_dataset for comparison
            url_path = request.path.split('/')
            if max(url_path) in valid_url:
                admin = self.authenticate(request)
                return admin

            # deny POST request if url is not in valid_url by default
            return False

        if request.method == 'PATCH':
            valid_url = ['edit_data']

            # splitting url e.g. /edit_data/1/ to get brain_dataset for comparison
            url_path = request.path.split('/')
            if max(url_path) in valid_url:
                admin = self.authenticate(request)
                return admin

            # deny PATCH request if url is not in valid_url by default
            return False

        return False

    # Check for auth_token length and pass it for decoding
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

    # Header for auth_token as `Token` instead of `Bearer`
    def authenticate_header(self, request):
        return 'Token'
