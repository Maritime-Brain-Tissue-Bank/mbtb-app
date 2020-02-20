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

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.valid_credentials = {
            'email': cls.admin_email,
            'password': cls.admin_password
        }
        cls.invalid_credentials = {
            'email': cls.admin_email,
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

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test GET, PATCH, requests
class NewUsersViewSetTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.test_1 = Users.objects.create(
            email='temp_1@gmail.com', first_name='temp', last_name='temp', institution='temp', department_name='temp',
            position_title='temp', city='temp', province='temp', country='temp')
        cls.valid_payload = {
            'pending_approval': 'N',
            'comments': 'asd'
        }
        cls.invalid_payload = {
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

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
