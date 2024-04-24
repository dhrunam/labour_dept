from rest_framework import serializers
from master import serializers as mst_serializer
from account import models as acc_model
from django.contrib.auth.models import User, Group
from django.contrib.auth import hashers

class UserProfileSerializer(serializers.ModelSerializer):
    # related_office = mst_serializer.OfficeDetailsSerializer(source="organization",many=False, read_only=True)
    class Meta:
        model = acc_model.UserProfile
        fields = (
            'id',
            'user',
            'organization',
            # 'name',
            'contact_number',
            'email',
            'gender',
            'id_proof',
            'document_type',
            'is_deleted'
        )

    def is_user_in_group(self, user, group_name):
        group = Group.objects.get(name=group_name)
        return user.groups.filter(name=group_name).exists()


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
        ]

class UserSerializer(serializers.ModelSerializer):
    related_profile = UserProfileSerializer(source='user_profile', many=False, read_only =True)
    related_group = UserGroupSerializer(source='groups', many=True, read_only =True)
  
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'related_profile',
            'related_group',
           
        ]

class   UserSerializerForRegistraion(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id', 
            'password', 
            'last_login', 
            'is_superuser', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'is_staff', 
            'is_active', 
            'date_joined',

        ]

    def validate(self, data):
        user = self.context['request'].user
      
        if user.check_password(data.get('password')):
            raise serializers.ValidationError("New password must be different from the old password.")

        if data.get('password'):
            data['password'] = hashers.make_password(data['password'])
        return data



class HelperUserSerializer(serializers.ModelSerializer):
    related_user_profile = UserProfileSerializer(source='user_profile',many=False,read_only=True)
    class Meta:
        model = User
        fields = ('id','username', 'related_user_profile')

class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_model.UserOTP
        fields = ('contact', 'otp','otp_date_time')