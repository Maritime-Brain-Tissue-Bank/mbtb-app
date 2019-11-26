from rest_framework import serializers
from .models import AutopsyTypes, PrimeDetails, OtherDetails, NeuropathologicalDiagnosis, \
    TissueTypes


class AutopsyTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutopsyTypes
        fields = "__all__"


# Serializer to have all mbtb_data from `BrainDataset` model
class PrimeDetailsSerializer(serializers.ModelSerializer):
    neuro_diagnosis_id = serializers.CharField(source='neuro_diagnosis_id.neuro_diagnosis_name', read_only=True)
    tissue_type = serializers.CharField(source='tissue_type.tissue_type', read_only=True)

    class Meta:
        model = PrimeDetails
        fields = "__all__"


# Serializer to have detailed view for a single record from `DatasetOthrDetails` model
class OtherDetailsSerializer(serializers.ModelSerializer):
    mbtb_code = serializers.CharField(source='prime_details_id.mbtb_code', read_only=True)
    sex = serializers.CharField(source='prime_details_id.sex', read_only=True)
    age = serializers.CharField(source='prime_details_id.age', read_only=True)
    postmortem_interval = serializers.CharField(source='prime_details_id.postmortem_interval', read_only=True)
    time_in_fix = serializers.CharField(source='prime_details_id.time_in_fix', read_only=True)
    neuro_diagnosis = serializers.CharField(source='prime_details_id.neuro_diagnosis_id', read_only=True)
    tissue_type = serializers.CharField(source='prime_details_id.tissue_type', read_only=True)
    preservation_method = serializers.CharField(source='prime_details_id.preservation_method', read_only=True)
    storage_year = serializers.CharField(source='prime_details_id.storage_year', read_only=True)
    autopsy_type = serializers.CharField(source='autopsy_type.autopsy_type', read_only=True)

    class Meta:
        model = OtherDetails
        fields = "__all__"
