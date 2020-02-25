from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import TissueRequests
from mbtb.models import AdminAccount, UserAccount
from .serializers import TissueRequestsSerializer
from resources.tests.common_tests import CommonTests
import jwt


# This class is to set up test data
class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_data_1 = {
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
        }  # For get new requests tests
        cls.test_data_2 = cls.test_data_1.copy()  # For get archive list tests
        cls.test_data_2['pending_approval'] = 'N'
        cls.model_response_1 = TissueRequests.objects.create(**cls.test_data_1)
        cls.model_response_2 = TissueRequests.objects.create(**cls.test_data_2)
        
        # Admin Authentication: generate temp account and admin_token
        cls.admin_email = 'admin@mbtb.ca'
        cls.admin_password = 'asdfghjkl123'
        AdminAccount.objects.create(email=cls.admin_email, password_hash=cls.admin_password)
        admin = AdminAccount.objects.get(email=cls.admin_email)
        admin_payload = {
            'id': admin.id,
            'email': admin.email,
        }
        cls.admin_token = jwt.encode(admin_payload, "SECRET_KEY", algorithm='HS256')  # generating jwt admin_token
        cls.admin_client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

        # User Account: for adding new tissue request, generating temp account and user token
        cls.user_email = 'user@mbtb.ca'
        cls.user_password = 'asdfghjkl1234'
        UserAccount.objects.create(email=cls.user_email, password_hash=cls.user_password)
        user = UserAccount.objects.get(email=cls.user_email)
        user_payload = {
            'id': user.id,
            'email': user.email,
        }
        cls.user_token = jwt.encode(user_payload, "SECRET_KEY", algorithm='HS256')  # generating jwt admin_token
        cls.user_client = APIClient(enforce_csrf_checks=True)  # enforcing csrf checks

    @classmethod
    def tearDownClass(cls):
        TissueRequests.objects.all().delete()
        AdminAccount.objects.all().delete()
        UserAccount.objects.all().delete()


# This class is to test PostNewTissueRequestsView as a user.
# Default: post request is allowed, and rest of them are blocked.
class PostNewTissueRequestsViewTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.invalid_payload = self.test_data_1.copy()
        self.invalid_payload['email'] = None
        self.common_tests = CommonTests(token=self.user_token, url='/add_new_tissue_requests/')

    # Valid post request
    def test_valid_new_request(self):
        self.user_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.decode('utf-8'))
        response = self.user_client.post('/add_new_tissue_requests/', self.test_data_1, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        model_response = TissueRequests.objects.filter(pending_approval='Y')
        self.assertEqual(len(model_response), 2)
        self.client.credentials()

    # Invalid post request
    def test_invalid_new_request(self):
        predicted_msg = 'This field may not be null.'
        self.user_client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.decode('utf-8'))
        response = self.user_client.post('/add_new_tissue_requests/', self.invalid_payload, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], predicted_msg)
        model_response = TissueRequests.objects.filter(pending_approval='Y')
        self.assertEqual(len(model_response), 1)
        self.client.credentials()

    def test_common_tests(self):
        # Invalid delete request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="delete", predicted_msg="not_allowed", response_tag="detail", http_response="405"), True)

        # Invalid get request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="get", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Invalid patch request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="patch", predicted_msg="not_allowed", response_tag="detail", http_response="405",
            data=self.test_data_1), True)

        # Test: with empty token for post request
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="post", predicted_msg="empty_token", response_tag="detail", data=self.test_data_1), True)

        # Test: with invalid token header for post request
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="post", predicted_msg="invalid_token_header", response_tag="detail", data=self.test_data_1),
            True)

        # Test: without token for post request
        self.assertEquals(self.common_tests.request_without_token(
            request_type="post", predicted_msg="invalid_token_header", response_tag="detail", data=self.test_data_1),
            True)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()
        del self.common_tests


# This class is to test GetNewTissueRequestsView as an admin.
# Default: get request is allowed, and rest of them are blocked.
class GetNewTissueRequestsViewTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.common_tests = CommonTests(token=self.admin_token, url='/get_new_tissue_requests/')

    # Valid get request to fetch all new tissue requests
    def test_get_all_new_tissue_request(self):
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get('/get_new_tissue_requests/')
        model_response = TissueRequests.objects.filter(pending_approval='Y')
        serializer_response = TissueRequestsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_client.credentials()

    # Valid get request to fetch new single tissue requests
    def test_get_single_tissue_request(self):
        url = '/get_new_tissue_requests/' + str(self.model_response_1.pk) + '/'
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get(url)
        model_response = TissueRequests.objects.get(pk=self.model_response_1.pk)
        serializer_response = TissueRequestsSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_client.credentials()

    # Invalid get single tissue request
    def test_get_invalid_single_request(self):
        url = '/get_new_tissue_requests/' + '25' + '/'
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.admin_client.credentials()

    # Test: valid delete request
    def test_delete_request(self):
        predicted_msg_1 = 'Not found.'
        predicted_msg_2 = 'Invalid input. Only `Token` tag is allowed.'
        response_without_token = self.admin_client.delete('/get_new_tissue_requests/1/')
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response_with_token = self.admin_client.delete('/get_new_tissue_requests/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg_1)
        self.assertEqual(response_without_token.data['detail'], predicted_msg_2)

    def test_common_tests(self):
        # ToDo: Fix common delete test here for invalid delete request

        # Invalid post request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="post", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Test: with empty token for get, patch requests
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="get", predicted_msg="empty_token", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="patch", predicted_msg="empty_token", response_tag="detail", data=self.test_data_1), True)

        # Test: with invalid token header for get, patch requests
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail",
            data=self.test_data_1), True)

        # Test: without token for get, patch requests
        self.assertEquals(self.common_tests.request_without_token(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_without_token(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail",
            data=self.test_data_1), True)
    
    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()
        del self.common_tests


# This class is to test GetArchiveTissueRequestsView as an admin.
# Default: get request is allowed, and rest of them are blocked.
class GetArchiveTissueRequestsViewTest(SetUpTestData):

    def setUp(self):
        super(SetUpTestData, self).setUpClass()
        self.common_tests = CommonTests(token=self.user_token, url='/get_archive_tissue_requests/')

    # Valid get request
    def test_get_all_new_tissue_request(self):
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get('/get_archive_tissue_requests/')
        model_response = TissueRequests.objects.filter(pending_approval='N')
        serializer_response = TissueRequestsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_client.credentials()

    # Test: valid get single item request
    def test_get_single_tissue_request(self):
        url = '/get_archive_tissue_requests/' + str(self.model_response_2.pk) + '/'
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get(url)
        model_response = TissueRequests.objects.get(pk=self.model_response_2.pk)
        serializer_response = TissueRequestsSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_client.credentials()

    # Test: invalid single item request
    def test_get_invalid_single_request(self):
        url = '/get_archive_tissue_requests/' + '25' + '/'
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.admin_client.credentials()

    # Test: delete request
    def test_delete_request(self):
        predicted_msg_1 = 'Not found.'
        predicted_msg_2 = 'Invalid input. Only `Token` tag is allowed.'
        response_without_token = self.admin_client.delete('/get_archive_tissue_requests/1/')
        self.admin_client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.decode('utf-8'))
        response_with_token = self.admin_client.delete('/get_archive_tissue_requests/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg_1)
        self.assertEqual(response_without_token.data['detail'], predicted_msg_2)

    def test_common_tests(self):
        # ToDo: Fix common delete test here for invalid delete request

        # Invalid post request
        self.assertEquals(self.common_tests.invalid_request_with_error_msg(
            request_type="post", predicted_msg="authorization", response_tag="detail", http_response="403"), True)

        # Test: with empty token for get, patch requests
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="get", predicted_msg="empty_token", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_with_empty_token(
            request_type="patch", predicted_msg="empty_token", response_tag="detail", data=self.test_data_1), True)

        # Test: with invalid token header for get, patch requests
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.invalid_token_header(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail",
            data=self.test_data_1), True)

        # Test: without token for get, patch requests
        self.assertEquals(self.common_tests.request_without_token(
            request_type="get", predicted_msg="invalid_token_header", response_tag="detail"), True)
        self.assertEquals(self.common_tests.request_without_token(
            request_type="patch", predicted_msg="invalid_token_header", response_tag="detail",
            data=self.test_data_1), True)

    def tearDown(self):
        super(SetUpTestData, self).tearDownClass()
        del self.common_tests
