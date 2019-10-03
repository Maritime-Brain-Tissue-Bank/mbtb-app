from rest_framework import serializers
from .models import AdminAccount, Users


class AdminAuthenticationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminAccount
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
