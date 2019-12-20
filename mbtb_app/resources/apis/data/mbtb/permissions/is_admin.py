from rest_framework import permissions, exceptions
from ..db_operations.user_or_admin import UserOrAdmin
from .base_operations import BaseOperations


# This class is to authenticate admin only, block remaining requests
class IsAdmin(permissions.BasePermission):

    # Allow following request from user
    def has_permission(self, request, view):

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

        if request.method == 'DELETE':
            valid_url = ['delete_data']

            # splitting url e.g. /delete_data/1/ to get brain_dataset for comparison
            url_path = request.path.split('/')
            if max(url_path) in valid_url:
                admin = self.authenticate(request)
                return admin

            # deny DELETE request if url is not in valid_url by default
            return False

        raise exceptions.MethodNotAllowed(method=request.method)

    def authenticate(self, request):
        # Validate request first, obtain response dict containing id and email.
        response = BaseOperations().validate_request(request)

        admin = UserOrAdmin(model_name='Admin').run(id=response['id'], email=response['email'])
        if admin:
            return True

        return False
