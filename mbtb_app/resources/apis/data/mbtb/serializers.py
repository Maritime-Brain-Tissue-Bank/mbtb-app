from rest_framework import serializers
from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType


class AutopsyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutopsyType
        fields = "__all__"


class BrainDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrainDataset
        fields = "__all__"


class DatasetOtherDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetOthrDetails
        fields = "__all__"


class ImageRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageRepository
        fields = "__all__"


class NeurodegenerativeDiseasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeurodegenerativeDiseases
        fields = "__all__"


class TissueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TissueType
        fields = "__all__"
