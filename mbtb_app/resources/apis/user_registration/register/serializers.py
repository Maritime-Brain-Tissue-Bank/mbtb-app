from rest_framework import serializers
from .models import NewUsers, NewUsersInfo, AdminAccount


class NewUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUsersInfo
        fields = ['id', 'address_line_1', 'address_line_2', 'city',
                  'province', 'postal_code', 'comments']


class NewUsersSerializer(serializers.ModelSerializer):
    new_users_info = NewUserInfoSerializer(many=True)

    class Meta:
        model = NewUsers
        fields = ['id', 'email', 'title', 'first_name', 'middle_name', 'last_name',
                  'organization', 'department', 'current_position', 'new_users_info']

    def create(self, validated_data):
        new_users_info_data = validated_data.pop('new_users_info')
        new_users = NewUsers.objects.create(**validated_data)
        for each_info in new_users_info_data:
            NewUsersInfo.objects.create(new_users=new_users, **each_info)
        return new_users


class AdminAuthenticationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminAccount
        fields = '__all__'
