from rest_framework import serializers
from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType


class AutopsyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutopsyType
        fields = "__all__"


class BrainDatasetSerializer(serializers.ModelSerializer):
    neuro_diseases = serializers.CharField(source='neuro_diseases.disease_name', read_only=True)
    tissue_type = serializers.CharField(source='tissue_type.tissue_type', read_only=True)

    class Meta:
        model = BrainDataset
        fields = "__all__"


class DatasetOtherDetailsSerializer(serializers.ModelSerializer):
    brain_data_id = serializers.CharField(source='brain_data_id.brain_data_id', read_only=True)
    autopsy_type = serializers.CharField(source='autopsy_type.autopsy_type', read_only=True)

    class Meta:
        model = DatasetOthrDetails
        fields = "__all__"


class ImageRepositorySerializer(serializers.ModelSerializer):
    brain_data_id = serializers.CharField(source='brain_data_id.brain_data_id', read_only=True)

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
