from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import AdminAccount
from users_api.models import Users
from users_api.serializers import UsersSerializer
import jwt


class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.admin_email = 'admin@mbtb.ca'
        cls.admin_password = 'asdfghjkl123'
        AdminAccount.objects.create(email=cls.admin_email, password_hash=cls.admin_password)
        admin = AdminAccount.objects.get(email=cls.admin_email)
        admin_auth_payload = {
            'id': admin.id,
            'email': admin.email
        }
        cls.token = jwt.encode(admin_auth_payload, "SECRET_KEY", algorithm='HS256')  # generating jwt token
        cls.client = APIClient(enforce_csrf_checks=True)  # Enforcing csrf checks

    @classmethod
    def tearDownClass(cls):
        AdminAccount.objects.all().delete()


# This class is to test admin login
class AdminAccountGetTokenViewTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.valid_credentials = {
            'email': self.admin_email,
            'password': self.admin_password
        }
        self.invalid_credentials = {
            'email': self.admin_email,
            'password': 'asdfghjklp123'
        }

    # post request with valid credentials
    def test_valid_admin_login(self):
        response = self.client.post(
            '/admin_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        _received_token = response._container[0].decode('utf-8')
        _decoded_token = jwt.decode(_received_token, "SECRET_KEY")
        _model_response = AdminAccount.objects.get(id=_decoded_token['id'], email=_decoded_token['email'])
        self.assertEqual(_model_response.email, self.admin_email)
        self.assertEqual(_model_response.password_hash, self.admin_password)

    # post request with invalid credentials
    def test_invalid_admin_login(self):
        _predicted_msg = 'Invalid username/password'
        response = self.client.post(
            '/admin_auth',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], _predicted_msg)

    # Invalid get request: should not be allowed
    def test_invalid_get_request(self):
        response = self.client.get(
            '/admin_auth/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    # Invalid patch request: should not be allowed
    def test_invalid_patch_request(self):
        response = self.client.patch(
            '/admin_auth/1/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    # Invalid delete request: should not be allowed
    def test_invalid_delete_request(self):
        response = self.client.delete(
            '/admin_auth/1/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()


# This class is to test GET, PATCH, requests
class NewUsersViewSetTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.test_1 = Users.objects.create(
            email='temp_1@gmail.com', first_name='temp', last_name='temp', institution='temp', department_name='temp',
            position_title='temp', city='temp', province='temp', country='temp')
        self.valid_payload = {
            'pending_approval': 'N',
            'comments': 'asd'
        }
        self.invalid_payload = {
            'email': '',
            'first_name': ''
        }
        self.common_tests = CommonTests(token=self.token, url='/list_new_users/')

    # get request with valid token
    def test_get_all_new_users_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/list_new_users/')
        new_users = Users.objects.all()
        new_users_serializer = UsersSerializer(new_users, many=True)
        self.assertEqual(response.data, new_users_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request for single user with valid token and payload data
    def test_get_single_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        new_users = Users.objects.get(pk=self.test_1.pk)
        new_users_serializer = UsersSerializer(new_users)
        self.assertEqual(response.data, new_users_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request for single user with valid token and invalid payload data
    def test_get_invalid_single_request(self):
        _predicted_msg = 'Not found.'
        url = '/list_new_users/' + '25' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], _predicted_msg)
        self.client.credentials()

    # patch request with valid token and data
    def test_patch_single_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pending_approval'], 'N')
        self.assertEqual(response.data['comments'], 'asd')
        self.client.credentials()

    # patch request with valid token but invalid payload data
    def test_patch_invalid_payload_request(self):
        _predicted_msg = 'This field may not be blank.'
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], _predicted_msg)
        self.assertEqual(response.data['first_name'][0], _predicted_msg)
        self.client.credentials()

    def test_common_tests(self):
        # Invalid post request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="post", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Invalid delete request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="delete", predicted_msg="not_allowed", response_tag="detail", http_response="405"), True)

        # Test: with empty token for get, patch requests
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="get", predicted_msg="empty_token", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="patch", predicted_msg="empty_token", response_tag="detail"), True)

        # Test: with invalid token header for get, patch requests
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

        # Test: without token for get, patch requests
        self.assertEquals(self.common_tests.request_without_token(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_without_token(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()


class CurrentUsersViewSetTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.current_user = Users.objects.create(
            email='current_user@gmail.com', first_name='temp', last_name='temp', institution='temp',
            department_name='temp', position_title='temp', city='temp', province='temp', country='temp',
            pending_approval='N', password_hash='asdfghjkl123'
        )
        self.valid_credentials = {
            'email': self.current_user.email,
            'password': self.current_user.password_hash
        }
        self.suspend_user_payload = {
            'suspend': 'Y'
        }
        self.common_tests = CommonTests(token=self.token, url='/current_users/')

    # Gets current users list and comparing with model data
    def test_get_current_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/current_users/')
        model_response = Users.objects.all()
        serializer_response = UsersSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # Gets single user detail and comparing with model data.
    def test_get_single_user(self):
        url = '/current_users/' + str(self.current_user.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = Users.objects.get(pk=self.current_user.pk)
        serializer_response = UsersSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # Invalid single user request: unknown user id
    def test_invalid_get_single_user(self):
        url = '/current_users/' + '23/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # This test first login with user then suspend the user account by sending patch request
    # Confirm it by comparing against received response, performing get request on same url, data fetched from model,
    # failed login attempt with suspension message.
    def test_suspend_user(self):
        _suspended_msg = 'Your account is suspended. Please contact admin.'
        _get_request_msg = 'Not found.'

        # testing normal user login before suspension, verifying by receiving auth_token.
        before_suspension_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(before_suspension_response.status_code, status.HTTP_200_OK)
        _received_token = before_suspension_response._container[0].decode('utf-8')
        _decoded_token = jwt.decode(_received_token, "SECRET_KEY")
        _model_response = Users.objects.get(id=_decoded_token['id'], email=_decoded_token['email'])
        self.assertEqual(_model_response.email, self.current_user.email)
        self.assertEqual(_model_response.password_hash, self.current_user.password_hash)

        # Suspending user account via patch request, confirming by received response.
        self.url = '/current_users/{}/'.format(self.current_user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        suspended_response = self.client.patch(self.url, self.suspend_user_payload, format='json')
        self.assertEqual(suspended_response.status_code, status.HTTP_200_OK)
        self.assertEqual(suspended_response.data['email'], self.current_user.email)
        self.assertEqual(suspended_response.data['suspend'], 'Y')

        # Performing get request to check response i.e. should be Not Found.
        get_request_response = self.client.get(self.url, format='json')
        self.assertEqual(get_request_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_request_response.data['detail'], _get_request_msg)
        self.client.credentials()

        # Confirming suspended account by fetching data directly from model
        _model_response = Users.objects.get(id=self.current_user.id)
        self.assertEqual(_model_response.email, self.current_user.email)
        self.assertEqual(_model_response.suspend, 'Y')

        # Failed login attempt with suspended account's credentials
        after_suspension_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(after_suspension_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(after_suspension_response.data['Error'], _suspended_msg)

    # Invalid suspend user test: unknown user id
    def test_invalid_suspend_user(self):
        _predicted_msg = 'Not found.'
        self.url = '/current_users/24/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(self.url, self.suspend_user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], _predicted_msg)

    def test_common_tests(self):
        # Invalid post request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="post", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Invalid delete request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="delete", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Test: with empty token for get, patch requests
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="get", predicted_msg="empty_token", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="patch", predicted_msg="empty_token", response_tag="detail"), True)

        # Test: with invalid token header for get, patch requests
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

        # Test: without token for get, patch requests
        self.assertEquals(self.common_tests.request_without_token(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_without_token(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()


class SuspendedUsersViewSetTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.current_user = Users.objects.create(
            email='current_user@gmail.com', first_name='temp', last_name='temp', institution='temp',
            department_name='temp', position_title='temp', city='temp', province='temp', country='temp',
            pending_approval='N', password_hash='asdfghjkl123', suspend='Y'
        )
        self.valid_credentials = {
            'email': self.current_user.email,
            'password': self.current_user.password_hash
        }
        self.revert_user_payload = {
            'suspend': 'N'
        }
        self.common_tests = CommonTests(token=self.token, url='/suspended_users/')

    # Gets suspended users list and comparing with model data
    def test_get_current_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/suspended_users/')
        model_response = Users.objects.all()
        serializer_response = UsersSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # Gets single user detail and comparing with model data.
    def test_get_single_user(self):
        url = '/suspended_users/' + str(self.current_user.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = Users.objects.get(pk=self.current_user.pk)
        serializer_response = UsersSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # Invalid request: no token
    def test_invalid_get_current_user(self):
        _predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.get('/suspended_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], _predicted_msg)

    # Invalid single user request: unknown user id
    def test_invalid_get_single_user(self):
        url = '/suspended_users/' + '232/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # This test first try to login with user should receive suspended message then
    # it reverts the user account by sending patch request
    # Confirm it by comparing against received response, performing get request on same url, data fetched from model,
    # successful login attempt with auth token.
    def test_suspend_user(self):
        _suspended_msg = 'Your account is suspended. Please contact admin.'
        _get_request_msg = 'Not found.'

        # Failed login attempt with suspended account's credentials
        after_suspension_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(after_suspension_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(after_suspension_response.data['Error'], _suspended_msg)

        # Reverting user account via patch request, confirming by received response.
        self.url = '/suspended_users/{}/'.format(self.current_user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        suspended_response = self.client.patch(self.url, self.revert_user_payload, format='json')
        self.assertEqual(suspended_response.status_code, status.HTTP_200_OK)
        self.assertEqual(suspended_response.data['email'], self.current_user.email)
        self.assertEqual(suspended_response.data['suspend'], 'N')

        # Performing get request to check response i.e. should be Not Found.
        get_request_response = self.client.get(self.url, format='json')
        self.assertEqual(get_request_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_request_response.data['detail'], _get_request_msg)
        self.client.credentials()

        # Confirming suspended account by fetching data directly from model
        _model_response = Users.objects.get(id=self.current_user.id)
        self.assertEqual(_model_response.email, self.current_user.email)
        self.assertEqual(_model_response.suspend, 'N')

        # testing normal user login before suspension, verifying by receiving auth_token.
        before_suspension_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(before_suspension_response.status_code, status.HTTP_200_OK)
        _received_token = before_suspension_response._container[0].decode('utf-8')
        _decoded_token = jwt.decode(_received_token, "SECRET_KEY")
        _model_response = Users.objects.get(id=_decoded_token['id'], email=_decoded_token['email'])
        self.assertEqual(_model_response.email, self.current_user.email)
        self.assertEqual(_model_response.password_hash, self.current_user.password_hash)

    # Invalid suspend user test: unknown user id
    def test_invalid_suspend_user(self):
        _predicted_msg = 'Not found.'
        self.url = '/suspended_users/242/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(self.url, self.revert_user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], _predicted_msg)

    def test_common_tests(self):
        # Invalid delete request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="delete", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Invalid post request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="post", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Test: with empty token for get, patch requests
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="get", predicted_msg="empty_token", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="patch", predicted_msg="empty_token", response_tag="detail"), True)

        # Test: with invalid token header for get, patch requests
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

        # Test: without token for get, patch requests
        self.assertEquals(self.common_tests.request_without_token(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_without_token(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail"), True)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()
        del self.common_tests


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
