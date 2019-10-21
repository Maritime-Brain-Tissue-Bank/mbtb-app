from django.shortcuts import render

# Create your views here.
from rest_framework import generics
# from rest_framework import viewsets
from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType
from .serializers import AutopsyTypeSerializer, BrainDatasetSerializer, DatasetOtherDetailsSerializer, \
    ImageRepositorySerializer, NeurodegenerativeDiseasesSerializer, TissueTypeSerializer


class AutopsyTypeAPIView(generics.ListCreateAPIView):
    queryset = AutopsyType.objects.all()
    serializer_class = AutopsyTypeSerializer


class BrainDatasetAPIView(generics.ListCreateAPIView):
    queryset = BrainDataset.objects.all()
    serializer_class = BrainDatasetSerializer


class DatasetOthrDetailsAPIView(generics.ListCreateAPIView):
    queryset = DatasetOthrDetails.objects.all()
    serializer_class = DatasetOtherDetailsSerializer


class ImageRepositoryAPIView(generics.ListCreateAPIView):
    queryset = ImageRepository.objects.all()
    serializer_class = ImageRepositorySerializer


class NeurodegenerativeDiseasesAPIView(generics.ListCreateAPIView):
    queryset = NeurodegenerativeDiseases.objects.all()
    serializer_class = NeurodegenerativeDiseasesSerializer


class TissueTypeAPIView(generics.ListCreateAPIView):
    queryset = TissueType.objects.all()
    serializer_class = TissueTypeSerializer
