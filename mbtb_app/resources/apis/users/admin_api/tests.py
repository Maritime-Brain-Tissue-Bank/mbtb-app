from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import AdminAccount
from users_api.models import Users
from users_api.serializers import UsersSerializer
import jwt


# This class is to test admin login
class AdminAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.email = 'admin@mbtb.ca'
        self.password = 'asdfghjkl123'
        AdminAccount.objects.create(email=self.email, password_hash=self.password)
        self.valid_credentials = {
            'email': self.email,
            'password': self.password
        }
        self.invalid_credentials = {
            'email': self.email,
            'password': 'asdfghjklp123'
        }
        self.client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

    # post request with valid credentials
    def test_valid_admin_login(self):
        response = self.client.post(
            '/admin_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # post request with invalid credentials
    def test_invalid_admin_login(self):
        response = self.client.post(
            '/admin_auth',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


# This class is to test GET, PATCH, requests
class NewUsersGetRequest(APITestCase):

    def setUp(self):
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
        self.email = 'admin@mbtb.ca'
        self.password = 'asdfghjkl123'
        AdminAccount.objects.create(email=self.email, password_hash=self.password)
        admin = AdminAccount.objects.get(email=self.email)
        payload = {
            'id': admin.id,
            'email': admin.email,
        }
        self.token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')  # generating jwt token
        self.client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

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
        response = self.client.get('/list_new_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        url = '/list_new_users/' + '25' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # patch request with valid token and data
    def test_patch_single_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # patch request with valid token but invalid payload data
    def test_patch_invalid_payload_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

    # patch request without token
    def test_patch_invalid_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
