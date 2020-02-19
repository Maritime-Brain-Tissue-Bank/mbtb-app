from rest_framework import permissions


# This class allows post request i.e. for new user registration
class IsPostAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests, no authentication
        if request.method == 'POST':
            return True

        return False
