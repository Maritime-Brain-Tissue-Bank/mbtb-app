from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import Users
from admin_signin.models import AdminAccount
from .serializers import UsersSerializer
import jwt


# This class is to test POST requests
class NewUserRequestTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "email": "amamam@gmail.com",
            "title": "Mr.",
            "first_name": "json",
            "middle_name": "",
            "last_name": "json",
            "institution": "dal",
            "department_name": "medical",
            "position_title": "developer",
            "address_line_1": "temp_location",
            "address_line_2": "",
            "city": "city",
            "province": "province",
            "country": "country",
            "postal_code": "postalcode",
            "comments": "this is comment box"
        }

        self.invalid_payload = {
            "email": "",
            "title": "Mr.",
            "first_name": "",
            "middle_name": "",
            "last_name": "",
            "institution": "dal",
            "department_name": "medical",
            "position_title": "developer",
            "address_line_1": "temp_location",
            "address_line_2": "",
            "city": "city",
            "province": "province",
            "country": "country",
            "postal_code": "postalcode",
            "comments": "this is comment box"
        }
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_valid_new_request(self):
        response = self.client.post(
            '/add_new_users/',
            self.valid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_valid_bad_new_request(self):
        response = self.client.post(
            '/add_new_users/',
            self.invalid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


# This class is to test GET, PATCH, requests
class NewUsersGetRequest(APITestCase):

    def setUp(self):
        self.test_1 = Users.objects.create(
            email='temp_1@gmail.com', first_name='temp', last_name='temp', institution='temp', department_name='temp',
            position_title='temp', city='temp', province='temp', country='temp')
        self.test_2 = Users.objects.create(
            email='temp_2@gmail.com', first_name='temp', last_name='temp', institution='temp', department_name='temp',
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
        self.token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
        self.client = APIClient(enforce_csrf_checks=True)

    def test_get_all_new_users_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/list_new_users/')
        new_users = Users.objects.all()
        new_users_serializer = UsersSerializer(new_users, many=True)
        self.assertEqual(response.data, new_users_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_get_invalid_request(self):
        response = self.client.get('/list_new_users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        new_users = Users.objects.get(pk=self.test_1.pk)
        new_users_serializer = UsersSerializer(new_users)
        self.assertEqual(response.data, new_users_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_get_invalid_single_request(self):
        url = '/list_new_users/' + '25' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    def test_patch_single_request(self):
        url = '/list_new_users/' + str(self.test_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_patch_invalid_payload_request(self):
        url = '/list_new_users/' + str(self.test_2.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(url, data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

    def test_patch_invalid_request(self):
        url = '/list_new_users/' + str(self.test_2.pk) + '/'
        response = self.client.patch(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)