from rest_framework import serializers
from operation import models as op_models

class ApplicationProgressHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = op_models.ApplicationProgressHistory
        fields = (
            'id',
            'application',
            'initiated_by',
            'remarks',
            'application_status',
            'created_at',
        )
