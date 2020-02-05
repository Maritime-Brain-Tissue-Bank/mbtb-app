from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import TissueRequests
from mbtb.models import AdminAccount, UserAccount
from .serializers import TissueRequestsSerializer
import jwt


# This class is to set up test data
class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@gmail.com",
            "institution": "dal",
            "department_name": "med",
            "city": "test",
            "province": "ns",
            "postal_code": "test",
            "project_title": "mbtb_app",
            "source_of_funding": "dal",
            "abstract": "test"
        }
        cls.model_response = TissueRequests.objects.create(**cls.test_data)
        # Admin Authentication: generate temp account and token
        cls.email = 'admin@mbtb.ca'
        cls.password = 'asdfghjkl123'
        AdminAccount.objects.create(email=cls.email, password_hash=cls.password)
        admin = AdminAccount.objects.get(email=cls.email)
        payload = {
            'id': admin.id,
            'email': admin.email,
        }
        cls.token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')  # generating jwt token
        cls.client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

    @classmethod
    def tearDownClass(cls):
        pass


class PostNewTissueRequestsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


class GetNewTissueRequestsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    def test_get_all_new_tissue_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/get_new_tissue_requests/')
        model_response = TissueRequests.objects.all()
        serializer_response = TissueRequestsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_invalid_request(self):
        predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.get('/get_new_tissue_requests/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], predicted_msg)

    def test_get_single_tissue_request(self):
        url = '/get_new_tissue_requests/' + str(self.model_response.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = TissueRequests.objects.get(pk=self.model_response.pk)
        serializer_response = TissueRequestsSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_get_invalid_single_request(self):
        url = '/get_new_tissue_requests/' + '25' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    def test_get_request_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.get('/get_new_tissue_requests/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_request_with_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_invalid_header = self.client.get('/get_new_tissue_requests/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)

    def test_post_request(self):
        predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.post('/get_new_tissue_requests/1/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/get_new_tissue_requests/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def test_delete_request(self):
        predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.delete('/get_new_tissue_requests/1/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/get_new_tissue_requests/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


class GetArchiveTissueRequestsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
