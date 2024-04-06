from rest_framework import serializers
from master import models as mst_models

class OfficeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = mst_models.OfficeType
        fields = (
            'type',
            'short_name',
            'is_deleted'
        )
