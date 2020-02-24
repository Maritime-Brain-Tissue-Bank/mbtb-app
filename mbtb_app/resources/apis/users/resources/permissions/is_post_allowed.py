from rest_framework import permissions, exceptions


# This class allows post request i.e. for new user registration
class IsPostAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests, no authentication
        if request.method == 'POST':
            valid_url = ['admin_auth', 'add_new_users', 'user_auth']

            url_path = request.path.split('/')

            if max(url_path) in valid_url:
                return True

            return False

        raise exceptions.MethodNotAllowed(method=request.method)
