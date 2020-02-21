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

    def test_invalid_get_request(self):
        response = self.client.get(
            '/admin_auth/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_patch_request(self):
        response = self.client.patch(
            '/admin_auth/1/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

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

    # get request with valid token
    def test_get_all_new_users_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/list_new_users/')
        new_users = Users.objects.all()
        new_users_serializer = UsersSerializer(new_users, many=True)
        self.assertEqual(response.data, new_users_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_invalid_request(self):
        _predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.get('/list_new_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], _predicted_msg)

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

    # patch request without token
    def test_patch_invalid_request(self):
        _predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], _predicted_msg)

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

    def test_get_current_users(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/current_users/')
        model_response = Users.objects.all()
        serializer_response = UsersSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_get_single_user(self):
        url = '/current_users/' + str(self.current_user.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = Users.objects.get(pk=self.current_user.pk)
        serializer_response = UsersSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_invalid_get_current_user(self):
        _predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.get('/current_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], _predicted_msg)

    def test_invalid_get_single_user(self):
        url = '/current_users/' + '23/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # This test first suspend the user account by sending patch request
    # Confirm it by comparing against received response, performing get request on same url, data fetched from model,
    # failed login attempt with suspension message.
    def test_suspend_user(self):
        _suspended_msg = 'Your account is suspended. Please contact admin.'
        _get_request_msg = 'Not found.'

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
        login_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(login_response.data['Error'], _suspended_msg)

    def test_invalid_suspend_user(self):
        _predicted_msg = 'Not found.'
        self.url = '/current_users/24/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(self.url, self.suspend_user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], _predicted_msg)

    def test_request_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.get('/current_users/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_invalid_header = self.client.get('/current_users/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)

    def test_invalid_post_request(self):
        _predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.post('/current_users/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/current_users/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], _predicted_msg)
        self.assertEqual(response_without_token.data['detail'], _predicted_msg)

    def test_invalid_delete_request(self):
        _predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.delete('/current_users/1/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/current_users/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], _predicted_msg)
        self.assertEqual(response_without_token.data['detail'], _predicted_msg)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()
