from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
import jwt


# This class consists base operations: perform validations on request, at last decode jwt token
class BaseOperations(object):

    # Check for auth_token length and pass it for decoding
    def validate_request(self, request):
        auth = get_authorization_header(request).split()

        # Validate request tag
        if not auth or auth[0].lower() != b'token':
            msg = 'Invalid input. Only `Token` tag is allowed.'
            raise exceptions.AuthenticationFailed(msg)

        # Validate request with only tag, empty token
        elif len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1]
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.decode_credentials(token)

    # Decode jwt token and return dict and raise decode error if any
    def decode_credentials(self, token):
        try:
            payload = jwt.decode(token, "SECRET_KEY")
            response = {
                'id': payload['id'],
                'email': payload['email']
            }
            return response
        except BaseException as error_msg:
            error_msg = 'Token - ' + str(error_msg)
            raise exceptions.AuthenticationFailed(error_msg)
