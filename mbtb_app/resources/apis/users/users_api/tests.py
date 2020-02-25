from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Users
from .serializers import UsersSerializer
import jwt


class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_email = 'user@mbtb.ca'
        cls.user_password = 'right_password'
        Users.objects.create(email=cls.user_email, password_hash=cls.user_password)
        cls.user = Users.objects.get(email=cls.user_email)
        user_auth_payload = {
            'id': cls.user.id,
            'email': cls.user.email
        }
        cls.token = jwt.encode(user_auth_payload, "SECRET_KEY", algorithm='HS256')  # generating jwt token
        cls.client = APIClient(enforce_csrf_checks=True)  # Enforcing csrf checks

    @classmethod
    def tearDownClass(cls):
        Users.objects.all().delete()


# This class is to test admin login
class UsersAuthenticationTestCase(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.valid_credentials = {
            'email': cls.user_email,
            'password': cls.user_password
        }
        cls.invalid_credentials = {
            'email': cls.user_email,
            'password': 'wrong_password'
        }

    # post request with valid credentials
    def test_valid_user_login(self):
        response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        _received_token = response._container[0].decode('utf-8')
        _decoded_token = jwt.decode(_received_token, "SECRET_KEY")
        _model_response = Users.objects.get(id=_decoded_token['id'], email=_decoded_token['email'])
        self.assertEqual(_model_response.email, self.user_email)
        self.assertEqual(_model_response.password_hash, self.user_password)

    # post request with invalid credentials
    def test_invalid_user_login(self):
        _predicted_msg = 'Invalid username/password'
        response = self.client.post(
            '/user_auth',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['Error'], _predicted_msg)

    def test_invalid_get_request(self):
        response = self.client.get(
            '/user_auth/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_patch_request(self):
        response = self.client.patch(
            '/user_auth/1/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_request(self):
        response = self.client.delete(
            '/user_auth/1/',
            self.invalid_credentials,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_suspended_user_login(self):
        _suspended_msg = 'Your account is suspended. Please contact admin.'
        Users.objects.filter(email=self.user.email).update(suspend='Y')
        login_response = self.client.post(
            '/user_auth',
            self.valid_credentials,
            format='json'
        )
        self.assertEquals(login_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(login_response.data['Error'], _suspended_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test POST requests for new user accounts
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
        # force authentication for api testing
        self.client.force_authenticate()

    # post request with valid data
    def test_valid_new_request(self):
        response = self.client.post(
            '/add_new_users/',
            self.valid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.valid_payload['email'])
        self.assertEqual(response.data['first_name'], self.valid_payload['first_name'])
        self.assertEqual(response.data['pending_approval'], 'Y')

    # post request with invalid data
    def test_valid_bad_new_request(self):
        _predicted_msg = 'This field may not be blank.'
        response = self.client.post(
            '/add_new_users/',
            self.invalid_payload,
            format='json'
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], _predicted_msg)
        self.assertEqual(response.data['first_name'][0], _predicted_msg)
        self.assertEqual(response.data['last_name'][0], _predicted_msg)
