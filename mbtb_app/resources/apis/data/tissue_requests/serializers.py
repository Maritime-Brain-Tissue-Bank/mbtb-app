from rest_framework import serializers
from .models import TissueRequests


class TissueRequestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TissueRequests
        fields = '__all__'
