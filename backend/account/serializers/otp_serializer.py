from account import models as acc_model
from rest_framework import serializers


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = acc_model.UserOTP
        fields = ('contact', 'otp','otp_date_time')