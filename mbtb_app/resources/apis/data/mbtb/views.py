from rest_framework import viewsets
from .permissions import IsAuthenticated

from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType
from .serializers import AutopsyTypeSerializer, BrainDatasetSerializer, DatasetOtherDetailsSerializer, \
    ImageRepositorySerializer, NeurodegenerativeDiseasesSerializer, TissueTypeSerializer


class AutopsyTypeAPIView(viewsets.ModelViewSet):
    queryset = AutopsyType.objects.all()
    serializer_class = AutopsyTypeSerializer


class BrainDatasetAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BrainDataset.objects.all()
    serializer_class = BrainDatasetSerializer


class DatasetOthrDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DatasetOthrDetails.objects.all()
    serializer_class = DatasetOtherDetailsSerializer


class ImageRepositoryAPIView(viewsets.ModelViewSet):
    queryset = ImageRepository.objects.all()
    serializer_class = ImageRepositorySerializer


class NeurodegenerativeDiseasesAPIView(viewsets.ModelViewSet):
    queryset = NeurodegenerativeDiseases.objects.all()
    serializer_class = NeurodegenerativeDiseasesSerializer


class TissueTypeAPIView(viewsets.ModelViewSet):
    queryset = TissueType.objects.all()
    serializer_class = TissueTypeSerializer
