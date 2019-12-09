from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import PrimeDetails, NeuropathologicalDiagnosis, TissueTypes, AutopsyTypes, OtherDetails
from .models import AdminAccount
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer
import jwt


# This class is to set up test data
class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.tissue_type_1 = TissueTypes.objects.create(tissue_type="brain")
        cls.neuro_diagnosis_1 = NeuropathologicalDiagnosis.objects.create(neuro_diagnosis_name="Mixed AD VAD")
        cls.autopsy_type_1 = AutopsyTypes.objects.create(autopsy_type="Brain")
        cls.prime_details_1 = PrimeDetails.objects.create(
            neuro_diagnosis_id=cls.neuro_diagnosis_1, tissue_type=cls.tissue_type_1, mbtb_code="BB00-001",
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
        OtherDetails.objects.all().delete()
        PrimeDetails.objects.filter().delete()
        TissueTypes.objects.filter().delete()
        NeuropathologicalDiagnosis.objects.filter().delete()
        AutopsyTypes.objects.filter().delete()
        AdminAccount.objects.all().delete()


# This class is to test BrainDatasetAPIView: all request
# Default: only get request is allowed with auth_token, remaining is blocked
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
        response = self.client.get('/brain_dataset/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + ' get request with valid token')
        response_invalid_header = self.client.get('/brain_dataset/')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)

    # post request with and without token
    def test_post_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/brain_dataset/1/')
        response_without_token = self.client.post('/brain_dataset/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    # delete request with and without token
    def test_delete_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/brain_dataset/1/')
        response_without_token = self.client.delete('/brain_dataset/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test DatasetOthrDetailsAPIView: all request
# Default: only get request is allowed with auth_token, remaining is blocked
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
        url = '/other_details/' + str(self.other_details_1.pk) + '/'
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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/other_details/1/')
        response_without_token = self.client.post('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    # delete request with and without token
    def test_delete_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.delete('/other_details/1/')
        response_without_token = self.client.delete('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


class CreateDataAPIViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()
        cls.test_data = {
            'mbtb_code': 'BB89-100',
            'sex': 'Male',
            'age': '70',
            'postmortem_interval': '12',
            'time_in_fix': 'Not known',
            'tissue_type': 'Brain',
            'preservation_method': 'Fresh Frozen',
            'autopsy_type': 'Brain',
            'neuropathology_diagnosis': "Mixed AD VAD",
            'race': '',
            'clinical_diagnosis': 'AD',
            'duration': 0,
            'clinical_details': 'AD',
            'cause_of_death': '',
            'brain_weight': 1080,
            'neuropathology_summary': 'AD SEVERE WITH ATROPHY, NEURONAL LOSS AND GLIOSIS',
            'neuropathology_gross': '',
            'neuropathology_microscopic': '',
            'cerad': '',
            'braak_stage': '',
            'khachaturian': '30',
            'abc': '',
            'formalin_fixed': 'True',
            'fresh_frozen': 'True'
        }

    def test_insert_data_(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    def test_insert_data_without_token(self):
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_data_check(self):
        self.test_data['tissue_type'] = ''
        self.test_data['autopsy_type'] = ''
        self.test_data['neuropathology_diagnosis'] = ''
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.credentials()

    def test_invalid_token_header(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + 'get request with valid token')
        response_invalid_header = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response_invalid_header.status_code, status.HTTP_403_FORBIDDEN)

    def test_request_with_empty_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + '')
        response_with_token = self.client.post('/add_new_data/', self.test_data, format='json')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
