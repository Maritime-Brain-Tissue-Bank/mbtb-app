from rest_framework import status
from rest_framework.test import APITestCase, APIClient


# This class perform common tests in order to avoid writing same code
class CommonTests(APITestCase):

    def __init__(self, **kwargs):
        super().__init__()
        self.common_client = APIClient(enforce_csrf_checks=True)
        self.predicted_msg = {
            'authorization': 'Authentication credentials were not provided.',
            'invalid_token_header': 'Invalid token header',
            'not_found': 'Not found.',
            'account_suspended': 'Your account is suspended. Please contact admin.',
            'no_token': 'Invalid input. Only `Token` tag is allowed.',
            'blank_field': 'This field may not be blank.',
            'empty_token': 'Invalid token header. No credentials provided.',
            'not_allowed': 'Method "{}" not allowed.'.format(kwargs.get('request_type', None))
        }
        self.http_response = {
            '403': status.HTTP_403_FORBIDDEN,
            '404': status.HTTP_404_NOT_FOUND,
            '405': status.HTTP_405_METHOD_NOT_ALLOWED
        }
        self.token = kwargs.get('token', None)
        self.url = kwargs.get('url', None)

    def invalid_request_with_error_msg(self, **kwargs):
        _predicted_msg = kwargs.get('predicted_msg', None)
        _request_type = kwargs.get('request_type', None)
        _data = kwargs.get('data', None)
        _response_check_tag = kwargs.get('response_tag', None)
        _http_response = kwargs.get('http_response', None)

        # Adding not allowed msg in predicted_msg dict.
        self.predicted_msg['not_allowed'] = 'Method "{}" not allowed.'.format(_request_type.upper())

        # generic requests with and without tokens
        response_without_token = self.common_client.generic(
            method=_request_type, path=self.url, data=_data, content_type='json'
        )
        self.common_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.common_client.generic(
            method=_request_type, path=self.url, data=_data, content_type='json'
        )
        self.assertEqual(response_with_token.status_code, self.http_response[_http_response])
        self.assertEqual(response_without_token.status_code, self.http_response[_http_response])
        self.assertEqual(response_with_token.data[_response_check_tag], self.predicted_msg[_predicted_msg])
        self.assertEqual(response_without_token.data[_response_check_tag], self.predicted_msg[_predicted_msg])
        return True

    def request_with_empty_token(self, **kwargs):
        _predicted_msg = kwargs.get('predicted_msg', None)
        _request_type = kwargs.get('request_type', None)
        _data = kwargs.get('data', None)
        _response_check_tag = kwargs.get('response_tag', None)
        self.common_client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.common_client.generic(
            method=_request_type, path=self.url, data=_data, content_type='json'
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data[_response_check_tag], self.predicted_msg[_predicted_msg])
        return True

    def invalid_token_header(self, **kwargs):
        _predicted_msg = kwargs.get('predicted_msg', None)
        _request_type = kwargs.get('request_type', None)
        _data = kwargs.get('data', None)
        _response_check_tag = kwargs.get('response_tag', None)
        self.common_client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_with_token = self.common_client.generic(
            method=_request_type, path=self.url, data=_data, content_type='json'
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data[_response_check_tag], self.predicted_msg[_predicted_msg])
        return True

    def request_without_token(self, **kwargs):
        _predicted_msg = kwargs.get('predicted_msg', None)
        _request_type = kwargs.get('request_type', None)
        _data = kwargs.get('data', None)
        _response_check_tag = kwargs.get('response_tag', None)
        response_with_token = self.common_client.generic(
            method=_request_type, path=self.url, data=_data, content_type='json'
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data[_response_check_tag], self.predicted_msg[_predicted_msg])
        return True
