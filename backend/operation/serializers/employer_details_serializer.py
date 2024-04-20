from rest_framework import serializers
from operation import models as op_models

class EmployerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = op_models.EmployerDetails
        fields = (
            'id',
            'application_certificate_establishment',
            'name',
            'designation',
            'designation',
            'permanent_address',
            )
        
