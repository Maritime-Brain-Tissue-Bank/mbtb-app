from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from django.db import transaction
from .models import BrainDataset, NeurodegenerativeDiseases, TissueType, AutopsyType, DatasetOthrDetails
from .models import AdminAccount
from .serializers import BrainDatasetSerializer, DatasetOtherDetailsSerializer
import jwt


# This class is to set up test data
class SetUpTestData(APITestCase):

    @classmethod
    def setUpClass(cls):
        cls.tissue_type_1 = TissueType.objects.create(tissue_type="brain")
        cls.neuro_diseases_1 = NeurodegenerativeDiseases.objects.create(disease_name="Mixed AD VAD")
        cls.autopsy_type_1 = AutopsyType.objects.create(autopsy_type="Brain")
        cls.brain_dataset_1 = BrainDataset.objects.create(
            neuoropathology_diagnosis=cls.neuro_diseases_1, tissue_type=cls.tissue_type_1, mbtb_code="BB00-001",
            sex="Female", age="92",
            postmortem_interval="15", time_in_fix="10", storage_method='Fresh Frozen',
            storage_year="2018-06-06T03:03:03",
            archive="No"
        )
        cls.datasetOthrDetails = DatasetOthrDetails.objects.create(
            brain_data_id=cls.brain_dataset_1, autopsy_type=cls.autopsy_type_1, race='test', diagnosis='test',
            duration=123, clinical_history='test', cause_of_death='test', brain_weight=123,
            neuoropathology_detailed='test', neuropathology_gross='test', neuropathology_micro='test',
            neouropathology_criteria='test', cerad='', abc='', khachaturian='', braak_stage='test',
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
        DatasetOthrDetails.objects.all().delete()
        BrainDataset.objects.filter().delete()
        TissueType.objects.filter().delete()
        NeurodegenerativeDiseases.objects.filter().delete()
        AutopsyType.objects.filter().delete()
        AdminAccount.objects.all().delete()


# This class is to test BrainDatasetAPIView: all request
# Default: only get request is allowed with auth_token, remaining is blocked
class BrainDatasetViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    # get request with valid token
    def test_get_all_brain_dataset(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/brain_dataset/')
        model_response = BrainDataset.objects.all()
        serializer_response = BrainDatasetSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_all_brain_dataset_invalid_request(self):
        response = self.client.get('/brain_dataset/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # get request for single brain_dataset with valid token and payload data
    def test_get_single_request(self):
        url = '/brain_dataset/' + str(self.brain_dataset_1.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = BrainDataset.objects.get(pk=self.brain_dataset_1.pk)
        serializer_response = BrainDatasetSerializer(model_response)
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

    # post request with and without token
    def test_post_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/brain_dataset/')
        response_without_token = self.client.post('/brain_dataset/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()


# This class is to test DatasetOthrDetailsAPIView: all request
# Default: only get request is allowed with auth_token, remaining is blocked
class DatasetOthrDetailsViewTest(SetUpTestData):

    def setUp(cls):
        super(SetUpTestData, cls).setUpClass()

    def test_get_all_othr_details(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/other_details/')
        model_response = DatasetOthrDetails.objects.all()
        serializer_response = DatasetOtherDetailsSerializer(model_response, many=True)
        self.assertEqual(response.data, serializer_response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials()

    # get request without token
    def test_get_all_othr_details_invalid_request(self):
        response = self.client.get('/other_details/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # get request for single other_details with valid token and payload data
    def test_get_single_request(self):
        url = '/other_details/' + str(self.datasetOthrDetails.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get(url)
        model_response = DatasetOthrDetails.objects.get(pk=self.datasetOthrDetails.pk)
        serializer_response = DatasetOtherDetailsSerializer(model_response)
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

    # post request with and without token
    def test_post_request(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response_with_token = self.client.post('/other_details/')
        response_without_token = self.client.post('/other_details/')
        self.assertEqual(response_with_token.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response_without_token.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(cls):
        super(SetUpTestData, cls).tearDownClass()
