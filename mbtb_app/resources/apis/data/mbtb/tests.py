from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import PrimeDetails, NeuropathologicalDiagnosis, TissueTypes, AutopsyTypes, OtherDetails
from .models import AdminAccount
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer, FileUploadPrimeDetailsSerializer, \
    FileUploadOtherDetailsSerializer, InsertRowPrimeDetailsSerializer
import jwt
import csv
import os


# This class is to set up test data
class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.tissue_type_1 = TissueTypes.objects.create(tissue_type="brain")
        cls.neuro_diagnosis_1 = NeuropathologicalDiagnosis.objects.create(neuro_diagnosis_name="Mixed AD VAD")
        cls.autopsy_type_1 = AutopsyTypes.objects.create(autopsy_type="Brain")
        cls.prime_details_1 = PrimeDetails.objects.create(
            neuro_diagnosis_id=cls.neuro_diagnosis_1, tissue_type=cls.tissue_type_1, mbtb_code="BB99-101",
            sex="Female", age="92", postmortem_interval="15", time_in_fix="10", preservation_method='Fresh Frozen',
            storage_year="2018-06-06T03:03:03", archive="No", clinical_diagnosis='test'
        )
        cls.other_details_1 = OtherDetails.objects.create(
            prime_details_id=cls.prime_details_1, autopsy_type=cls.autopsy_type_1, race='test',
            duration=123, clinical_details='test', cause_of_death='test', brain_weight=123,
            neuropathology_summary='test', neuropathology_gross='test', neuropathology_microscopic='test',
            cerad='', abc='', khachaturian='', braak_stage='test',
            formalin_fixed=True, fresh_frozen=True,
        )
        cls.test_data = {
            'mbtb_code': 'BB99-102', 'sex': 'Male', 'age': '70', 'postmortem_interval': '12',
            'time_in_fix': 'Not known', 'tissue_type': 'Brain', 'preservation_method': 'Fresh Frozen',
            'autopsy_type': 'Brain', 'neuropathology_diagnosis': "Mixed AD VAD", 'race': '',
            'clinical_diagnosis': 'AD', 'duration': "10", 'clinical_details': 'AD', 'cause_of_death': '',
            'brain_weight': "1080", 'neuropathology_summary': 'AD SEVERE WITH ATROPHY, NEURONAL LOSS AND GLIOSIS',
            'neuropathology_gross': '', 'neuropathology_microscopic': '', 'cerad': '', 'braak_stage': '',
            'khachaturian': '30', 'abc': '', 'formalin_fixed': 'True', 'fresh_frozen': 'True',
            'storage_year': '2018-06-06 03:03:03'
        }

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

    # Create CSV file once filename and data is provided
    def dict_to_csv_file(self, filename, data):
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)

    @classmethod
    def tearDownClass(cls):
        OtherDetails.objects.all().delete()
        PrimeDetails.objects.filter().delete()
        TissueTypes.objects.filter().delete()
        NeuropathologicalDiagnosis.objects.filter().delete()
        AutopsyTypes.objects.filter().delete()
        AdminAccount.objects.all().delete()
        del cls.test_data


# This class is to test PrimeDetailsAPIView: all request
# Default: only GET request is allowed with auth_token, remaining requests are blocked
class PrimeDetailsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    # get request with valid token
    def test_get_all_brain_dataset(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/brain_dataset/')
        model_response = PrimeDetails.objects.all()
        serializer_response = PrimeDetailsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_all_brain_dataset_invalid_request(self):
        predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.get('/brain_dataset/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], predicted_msg)

    # get request for single brain_dataset with valid token and payload data
    def test_get_single_request(self):
        url = '/brain_dataset/' + str(self.prime_details_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = PrimeDetails.objects.get(pk=self.prime_details_1.pk)
        serializer_response = PrimeDetailsSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request for single brain_dataset with valid token and invalid payload data
    def test_get_invalid_single_request(self):
        url = '/brain_dataset/' + '25' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # get request with empty token
    def test_get_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.get('/brain_dataset/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    # get request with invalid token header
    def test_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_invalid_header = self.client.get('/brain_dataset/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)

    # post request with and without token
    def test_post_request(self):
        predicted_msg = 'Method "POST" not allowed.'
        response_without_token = self.client.post('/brain_dataset/1/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/brain_dataset/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    # delete request with and without token
    def test_delete_request(self):
        predicted_msg = 'Method "DELETE" not allowed.'
        response_without_token = self.client.delete('/brain_dataset/1/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/brain_dataset/1/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test OtherDetailsAPIView: all request
# Default: only GET request is allowed with auth_token, remaining requests are blocked
class OtherDetailsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    #  get request with valid token
    def test_get_all_othr_details(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/other_details/')
        model_response = OtherDetails.objects.all()
        serializer_response = OtherDetailsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_all_othr_details_invalid_request(self):
        response = self.client.get('/other_details/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # get request for single other_details with valid token and payload data
    def test_get_single_request(self):
        url = '/other_details/' + str(self.prime_details_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = OtherDetails.objects.get(pk=self.other_details_1.pk)
        serializer_response = OtherDetailsSerializer(model_response)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request for single other_details with valid token and invalid payload data
    def test_get_invalid_single_request(self):
        url = '/other_details/' + '50' + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.credentials()

    # get request with empty token
    def test_get_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.get('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    # get request with invalid token header
    def test_invalid_token_header(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_invalid_header = self.client.get('/other_details/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)

    # post request with and without token
    def test_post_request(self):
        predicted_msg = 'Method "POST" not allowed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/other_details/1/')
        response_without_token = self.client.post('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    # delete request with and without token
    def test_delete_request(self):
        predicted_msg = 'Method "DELETE" not allowed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/other_details/1/')
        response_without_token = self.client.delete('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test CreateDataAPIView: all request
# Default: only POST request is allowed with auth_token, remaining requests are blocked
class CreateDataAPIViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.test_data['duration'] = "123"
        cls.changed_column_names = cls.test_data.copy()
        cls.changed_column_names['durations'] = cls.changed_column_names.pop('duration')
        cls.prime_details_error = cls.test_data.copy()
        cls.other_details_error = cls.test_data.copy()
        cls.is_number_check_error = cls.test_data.copy()
        cls.prime_details_error['mbtb_code'] = None
        cls.other_details_error['khachaturian'] = False
        cls.is_number_check_error['duration'] = 'test'

    # valid post request with token to insert data
    def test_insert_data_(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Response'], 'Success')
        self.client.credentials()

        # Fetch prime_details and other_details for mbtb_code `BB99-103` and compare its length
        model_response_prime_details = PrimeDetails.objects.get(mbtb_code='BB99-102')
        model_response_other_details = OtherDetails.objects.get(
            prime_details_id=model_response_prime_details.prime_details_id
        )
        serializer_response_prime_details = InsertRowPrimeDetailsSerializer(model_response_prime_details)
        serializer_response_other_details = FileUploadOtherDetailsSerializer(model_response_other_details)
        set_test_data = set(self.test_data)
        set_prime_details = set(serializer_response_prime_details.data)
        set_other_details = set(serializer_response_other_details.data)
        self.assertEqual(len(set_prime_details.intersection(set_test_data)), 8)
        self.assertEqual(len(set_other_details.intersection(set_test_data)), 15)

    # post request without token
    def test_insert_data_without_token(self):
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # post request with invalid data
    def test_invalid_data_check(self):
        self.test_data['mbtb_code'] = ''
        self.test_data['sex'] = ''
        self.test_data['duration'] = ''
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

    def test_prime_details_error(self):
        predicted_msg = 'Error in prime_details, Inserting data failed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_prime_details_error = self.client.post('/add_new_data/', self.prime_details_error, format='json')
        self.assertEqual(response_prime_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_prime_details_error.data['Error'], predicted_msg)
        self.client.credentials()

    def test_other_details_error(self):
        self.other_details_error['mbtb_code'] = 'test'
        predicted_msg = 'Error in other_details, Inserting data failed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_other_details_error = self.client.post('/add_new_data/', self.other_details_error, format='json')
        self.assertEqual(response_other_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_other_details_error.data['Error'], predicted_msg)
        self.client.credentials()

    # post request with invalid token header
    def test_invalid_token_header(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'get request with valid token')
        response_invalid_header = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)

    # post request with empty token
    def test_request_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    def test_column_names(self):
        predicted_msg = "Column names don't match with following: ['duration'], Please try again with valid names."
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_changed_names = self.client.post('/add_new_data/', self.changed_column_names, format='json')
        self.assertEqual(response_changed_names.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_changed_names.data['Error'], predicted_msg)
        self.client.credentials()

    def test_is_number_check(self):
        self.is_number_check_error['mbtb_code'] = 'test'
        predicted_msg = 'Expecting value, received text.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_is_number_check_error = self.client.post('/add_new_data/', self.is_number_check_error, format='json')
        self.assertEqual(response_is_number_check_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_is_number_check_error.data['Error'], predicted_msg)
        self.client.credentials()

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
        del cls.changed_column_names
        del cls.prime_details_error
        del cls.other_details_error


# This class is to test GetSelectOptions: all request
# Default: only get request is allowed with auth_token, remaining requests are blocked
class GetSelectOptionsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

        # Fetch following values: autopsy_type, tissue_type, neuropathology_diagnosis for comparison
        _neuropathology_diagnosis = NeuropathologicalDiagnosis.objects.values_list('neuro_diagnosis_name', flat=True) \
            .order_by('neuro_diagnosis_name')
        _autopsy_type = AutopsyTypes.objects.values_list('autopsy_type', flat=True).order_by('autopsy_type')
        _tissue_type = TissueTypes.objects.values_list('tissue_type', flat=True).order_by('tissue_type')
        cls.valid_response = {
            "neuropathology_diagnosis": _neuropathology_diagnosis,
            "autopsy_type": _autopsy_type,
            "tissue_type": _tissue_type
        }

    # get request to fetch valid data
    def test_get_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/get_select_options/')
        self.assertQuerysetEqual(response.data, self.valid_response, transform=lambda x: x)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_data_without_token(self):
        response = self.client.get('/get_select_options/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # get request with invalid token header
    def test_invalid_token_header(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with invalid token')
        response_invalid_header = self.client.get('/get_select_options/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)

    # get request with empty token
    def test_get_request_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.get('/get_select_options/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    # invalid post request test
    def test_post_request(self):
        predicted_msg = 'Method "POST" not allowed.'
        response_without_token = self.client.post('/get_select_options/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/get_select_options/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    # invalid delete request test
    def test_delete_request(self):
        predicted_msg = 'Method "DELETE" not allowed.'
        response_without_token = self.client.delete('/get_select_options/')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/get_select_options/')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
        del cls.valid_response


# This class is to test FileUploadAPIView: all request
# Default: only post request is allowed with auth_token, remaining requests are blocked
class FileUploadAPIViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.file_upload_data = cls.test_data.copy()
        del cls.file_upload_data['preservation_method']
        cls.file_upload_data['mbtb_code'] = 'BB99-103'

        # prime_details and other_details data with error in datatype
        cls.prime_details_error = cls.file_upload_data.copy()
        cls.other_details_error = cls.file_upload_data.copy()
        cls.missing_fields_error = cls.file_upload_data.copy()
        cls.changed_column_names = cls.file_upload_data.copy()
        cls.prime_details_error['storage_year'] = ''
        cls.other_details_error['duration'] = None
        del cls.missing_fields_error['duration']
        cls.changed_column_names['durations'] = cls.changed_column_names.pop('duration')

        # Creating csv files for FileUploadAPIViewTest
        cls.dict_to_csv_file('file_upload_test.csv', cls.file_upload_data)
        cls.dict_to_csv_file('file_upload_test.txt', cls.file_upload_data)
        cls.dict_to_csv_file('prime_details_error.csv', cls.prime_details_error)
        cls.dict_to_csv_file('other_details_error.csv', cls.other_details_error)
        cls.dict_to_csv_file('empty_file.csv', {})
        cls.dict_to_csv_file('missing_fields.csv', cls.missing_fields_error)
        cls.dict_to_csv_file('changed_column_names.csv', cls.changed_column_names)

    def test_data_upload(self):
        # Upload data and check status code and response
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.post(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Response'], 'Success')
        self.client.credentials()

        # Fetch prime_details and other_details for mbtb_code `BB99-103` and compare its length
        model_response_prime_details = PrimeDetails.objects.get(mbtb_code='BB99-103')
        model_response_other_details = OtherDetails.objects.get(
            prime_details_id=model_response_prime_details.prime_details_id
        )
        serializer_response_prime_details = FileUploadPrimeDetailsSerializer(model_response_prime_details)
        serializer_response_other_details = FileUploadOtherDetailsSerializer(model_response_other_details)
        set_file_upload_data = set(self.file_upload_data)
        set_prime_details = set(serializer_response_prime_details.data)
        set_other_details = set(serializer_response_other_details.data)
        self.assertEqual(len(set_prime_details.intersection(set_file_upload_data)), 8)
        self.assertEqual(len(set_other_details.intersection(set_file_upload_data)), 15)

    # post request without token
    def test_data_upload_without_token(self):
        predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.post(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], predicted_msg)
        self.client.credentials()

    # post request with invalid token
    def test_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with invalid token')
        response_invalid_header = self.client.post(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)

    # post request with empty token
    def test_request_with_empty_token(self):
        predicted_msg = 'Invalid token header. No credentials provided.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.post(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)

    # invalid data test with error in prime details
    def test_prime_details_error(self):
        predicted_msg = 'Error in prime details, Data uploading failed at mbtb_code: BB99-103'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_prime_details_error = self.client.post(
            '/file_upload/', {'file': open('prime_details_error.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_prime_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_prime_details_error.data['Response'], 'Failure')
        self.assertEqual(response_prime_details_error.data['Message'], predicted_msg)
        self.assertGreater(len(response_prime_details_error.data['Error']), 0)
        self.client.credentials()

    # invalid data test with error in other details
    def test_other_details_error(self):
        predicted_msg = 'Error in other details, Data uploading failed at mbtb_code: BB99-103'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_other_details_error = self.client.post(
            '/file_upload/', {'file': open('other_details_error.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_other_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_other_details_error.data['Response'], 'Failure')
        self.assertEqual(response_other_details_error.data['Message'], predicted_msg)
        self.assertGreater(len(response_other_details_error.data['Error']), 0)
        self.client.credentials()

    # test: without `file` tag or empty `file` tag
    def test_file_not_found(self):
        predicted_msg_1 = "File not found, please upload CSV file"
        predicted_msg_2 = "File can't be empty, Please upload again."
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        resposne_no_file_tag = self.client.post(
            '/file_upload/', {'no_file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        response_empty_file_tag = self.client.post(
            '/file_upload/', {'file': ''}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(resposne_no_file_tag.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_empty_file_tag.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposne_no_file_tag.data['Error'], predicted_msg_1)
        self.assertEqual(response_empty_file_tag.data['Error'], predicted_msg_2)
        self.client.credentials()

    def test_file_type(self):
        predicted_msg = 'Wrong file type, please upload CSV file'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        resposne_no_file_extension = self.client.post(
            '/file_upload/', {'file': open('file_upload_test.txt', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(resposne_no_file_extension.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposne_no_file_extension.data['Error'], predicted_msg)
        self.client.credentials()

    def test_file_size(self):
        predicted_msg_1 = 'Error in file size, please upload valid file.'
        predicted_msg_2 = 'Not enough elements are present in single row.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        resposne_empty_file = self.client.post(
            '/file_upload/', {'file': open('empty_file.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        response_missing_data = self.client.post(
            '/file_upload/', {'file': open('missing_fields.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(resposne_empty_file.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_missing_data.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposne_empty_file.data['Error'], predicted_msg_1)
        self.assertEqual(response_missing_data.data['Error'], predicted_msg_2)
        self.client.credentials()

    def test_column_names(self):
        predicted_msg = "Column names don't match with following: ['duration'], Please try again with valid names."
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        resposne_changed_names = self.client.post(
            '/file_upload/', {'file': open('changed_column_names.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(resposne_changed_names.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resposne_changed_names.data['Error'], predicted_msg)
        self.client.credentials()

    # invalid get request test
    def test_get_request(self):
        predicted_msg = 'Method "GET" not allowed.'
        response_without_token = self.client.get(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.get(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    # invalid delete request test
    def test_delete_request(self):
        predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.delete(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete(
            '/file_upload/', {'file': open('file_upload_test.csv', 'rb')}, headers={'Content-Type': 'text/csv'}
        )
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
        os.remove('file_upload_test.csv')  # Removing csv files
        os.remove('prime_details_error.csv')
        os.remove('other_details_error.csv')
        os.remove('file_upload_test.txt')
        os.remove('empty_file.csv')
        os.remove('missing_fields.csv')
        os.remove('changed_column_names.csv')
        del cls.prime_details_error
        del cls.other_details_error
        del cls.changed_column_names
        del cls.missing_fields_error


# This class is to test EditDataAPIView: all request
# Default: only PATCH request is allowed with auth_token, remaining requests are blocked
class EditDataAPIViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.test_data['sex'] = 'Female'
        cls.test_data['duration'] = "123"
        cls.url = '/edit_data/{}/'.format(cls.prime_details_1.prime_details_id)
        cls.changed_column_names = cls.test_data.copy()
        cls.changed_column_names['durations'] = cls.changed_column_names.pop('duration')
        cls.prime_details_error = cls.test_data.copy()
        cls.other_details_error = cls.test_data.copy()
        cls.is_number_check_error = cls.test_data.copy()
        cls.prime_details_error['mbtb_code'] = None
        cls.other_details_error['khachaturian'] = False
        cls.is_number_check_error['duration'] = 'test'

    def test_edit_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.patch(self.url, self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Response'], 'Success')
        self.client.credentials()
        prime_details_model_response = PrimeDetails.objects.get(prime_details_id=self.prime_details_1.prime_details_id)
        other_details_model_response = OtherDetails.objects.get(prime_details_id=self.prime_details_1.prime_details_id)
        self.assertEqual(prime_details_model_response.sex, self.test_data['sex'])
        self.assertEqual(str(other_details_model_response.duration), self.test_data['duration'])

    def test_edit_data_without_token(self):
        predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.patch(self.url, self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], predicted_msg)
        self.client.credentials()

    def test_prime_details_error(self):
        predicted_msg = 'Error in prime_details, Uploading data failed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_prime_details_error = self.client.patch(self.url, self.prime_details_error, format='json')
        self.assertEqual(response_prime_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_prime_details_error.data['Error'], predicted_msg)
        self.client.credentials()

    def test_other_details_error(self):
        predicted_msg = 'Error in other details, Uploading data failed.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_other_details_error = self.client.patch(self.url, self.other_details_error, format='json')
        self.assertEqual(response_other_details_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_other_details_error.data['Error'], predicted_msg)
        self.client.credentials()

    def test_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with invalid token')
        response_invalid_header = self.client.patch(self.url, self.test_data, format='json')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)

    def test_request_with_empty_token(self):
        predicted_msg = 'Invalid token header. No credentials provided.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.patch(self.url, self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)

    def test_column_names(self):
        predicted_msg = "Column names don't match with following: ['duration'], Please try again with valid names."
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_changed_names = self.client.patch(self.url, self.changed_column_names, format='json')
        self.assertEqual(response_changed_names.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_changed_names.data['Error'], predicted_msg)
        self.client.credentials()

    def test_get_request(self):
        predicted_msg = 'Method "GET" not allowed.'
        response_without_token = self.client.get(self.url, self.changed_column_names, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.get(self.url, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def test_post_request(self):
        predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.post(self.url, self.changed_column_names, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post(self.url, self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def test_put_request(self):
        predicted_msg = 'Method "PUT" not allowed.'
        response_without_token = self.client.put(self.url, self.changed_column_names, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.put(self.url, self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def test_is_number_check(self):
        self.is_number_check_error['mbtb_code'] = 'test'
        predicted_msg = 'Expecting value, received text.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_is_number_check_error = self.client.patch(self.url, self.is_number_check_error, format='json')
        self.assertEqual(response_is_number_check_error.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_is_number_check_error.data['Error'], predicted_msg)
        self.client.credentials()

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
        del cls.changed_column_names
        del cls.prime_details_error
        del cls.other_details_error
        del cls.url


# This class is to test DeleteDataAPIView: all request
# Default: only PATCH request is allowed with auth_token, remaining requests are blocked
class DeleteDataAPIViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.url = '/delete_data/{}/'.format(cls.prime_details_1.prime_details_id)

    def test_delete_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        delete_response = self.client.delete(self.url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.data['Response'], 'Success')
        self.client.credentials()
        model_response = PrimeDetails.objects.all().values_list()
        self.assertEqual(len(model_response), 0)

    def test_invalid_delete_request(self):
        _url = '/delete_data/101/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        delete_response = self.client.delete(_url, format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete_response.data['detail'], 'Not found.')

    def test_request_without_token(self):
        predicted_msg = 'Invalid input. Only `Token` tag is allowed.'
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], predicted_msg)
        self.client.credentials()

    def test_request_with_empty_token(self):
        predicted_msg = 'Invalid token header. No credentials provided.'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.delete(self.url, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.client.credentials()

    def test_invalid_token_header(self):
        predicted_msg = 'Invalid token header'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with invalid token')
        response_invalid_header = self.client.delete(self.url, format='json')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_invalid_header.data['detail'], predicted_msg)
        self.client.credentials()

    def test_get_request(self):
        predicted_msg = 'Method "GET" not allowed.'
        response_without_token = self.client.get(self.url, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.get(self.url, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_without_token.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def test_post_request(self):
        predicted_msg = 'Authentication credentials were not provided.'
        response_without_token = self.client.post(self.url, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post(self.url, self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_with_token.data['detail'], predicted_msg)
        self.assertEqual(response_without_token.data['detail'], predicted_msg)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
