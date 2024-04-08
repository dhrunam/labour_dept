from rest_framework import serializers
from operation  import models as op_models

class ManagementLevelEmployeeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = op_models.ManagementLevelEmployeeDetails
        fields = (
            'id',
            'application_certificate_establishment',
            'name',
            'age',
            'gender',
            'relationship',
        )