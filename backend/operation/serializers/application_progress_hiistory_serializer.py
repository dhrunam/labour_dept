from rest_framework import serializers
from operation import models as op_models
from account import serializers as acc_serializer

class ApplicationProgressHistorySerializer(serializers.ModelSerializer):
    related_initiated_by = acc_serializer.UserSerializer(source="initiated_by", many=False, read_only=True)
    class Meta:
        model = op_models.ApplicationProgressHistory
        fields = (
            'id',
            'application',
            'initiated_by',
            'remarks',
            'application_status',
            'created_at',
            'related_initiated_by',
        )
