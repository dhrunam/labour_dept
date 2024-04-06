from rest_framework import serializers
from operation import models as op_models

class EmployerParentageDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = op_models.EmployerParentageDetails
        fields = (  
                    'id',
                    'application_certificate_establishment',
                    'parentage_name',
                    'designation',
                    'permanent_address',
                    'nature_interest',
                  )


