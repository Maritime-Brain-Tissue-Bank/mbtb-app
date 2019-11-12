from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from .models import BrainDataset, NeurodegenerativeDiseases, TissueType
from .models import AdminAccount
from .serializers import BrainDatasetSerializer
import jwt


# This class is to test BrainDatasetAPIView: all request
# Default: only get request is allowed with auth_token, remaining is blocked
class BrainDatasetViewTest(APITestCase):

    def setUp(self):
        self.tissue_type_1 = TissueType.objects.create(tissue_type="brain")
        self.neuro_diseases_1 = NeurodegenerativeDiseases.objects.create(disease_name="Mixed AD VAD")
        self.brain_dataset_1 = BrainDataset.objects.create(
            neuoropathology_diagnosis=self.neuro_diseases_1, tissue_type=self.tissue_type_1, mbtb_code="BB00-001", sex="Female", age="92",
            postmortem_interval="15", time_in_fix="10", storage_method='Fresh Frozen', storage_year="2018-06-06T03:03:03",
            archive="No"
        )
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
    def test_get_all_brain_dataset(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.decode('utf-8'))
        response = self.client.get('/brain_dataset/')
        new_users = BrainDataset.objects.all()
        new_users_serializer = BrainDatasetSerializer(new_users, many=True)
        self.assertEqual(response.data, new_users_serializer.data)
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
        new_users = BrainDataset.objects.get(pk=self.brain_dataset_1.pk)
        new_users_serializer = BrainDatasetSerializer(new_users)
        self.assertEqual(response.data, new_users_serializer.data)
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
