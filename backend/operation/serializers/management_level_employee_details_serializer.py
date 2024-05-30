from rest_framework import serializers
from operation  import models as op_models

class ManagementLevelEmployeeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = op_models.ManagementLevelEmployeeDetails
        fields = (
            'id',
            'application',
            'name',
            'age',
            'gender',
            'relationship',
        )