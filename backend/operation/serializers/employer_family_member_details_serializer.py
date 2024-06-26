from rest_framework import serializers
from operation import models as op_models

class EmployerFamilyMemberDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = op_models.EmployerFamilyMemberDetails
        fields = (
            'id',
            'application',
            'name',
            'age',
            'gender',
            'relationship',
        )
