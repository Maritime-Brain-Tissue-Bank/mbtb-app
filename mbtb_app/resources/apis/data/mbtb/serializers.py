from rest_framework import serializers
from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType


class AutopsyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutopsyType
        fields = "__all__"


# Serializer to have all mbtb_data from `BrainDataset` model
class BrainDatasetSerializer(serializers.ModelSerializer):
    neuro_diseases_id = serializers.CharField(source='neuro_diseases_id.disease_name', read_only=True)
    tissue_type = serializers.CharField(source='tissue_type.tissue_type', read_only=True)

    class Meta:
        model = BrainDataset
        fields = "__all__"


# Serializer to have detailed view for a single record from `DatasetOthrDetails` model
class DatasetOtherDetailsSerializer(serializers.ModelSerializer):
    mbtb_code = serializers.CharField(source='brain_data_id.mbtb_code', read_only=True)
    sex = serializers.CharField(source='brain_data_id.sex', read_only=True)
    age = serializers.CharField(source='brain_data_id.age', read_only=True)
    postmortem_interval = serializers.CharField(source='brain_data_id.postmortem_interval', read_only=True)
    time_in_fix = serializers.CharField(source='brain_data_id.time_in_fix', read_only=True)
    neuoropathology_diagnosis = serializers.CharField(source='brain_data_id.neuro_diseases_id', read_only=True)
    tissue_type = serializers.CharField(source='brain_data_id.tissue_type', read_only=True)
    storage_method = serializers.CharField(source='brain_data_id.storage_method', read_only=True)
    storage_year = serializers.CharField(source='brain_data_id.storage_year', read_only=True)
    autopsy_type = serializers.CharField(source='autopsy_type.autopsy_type', read_only=True)

    class Meta:
        model = DatasetOthrDetails
        fields = "__all__"
