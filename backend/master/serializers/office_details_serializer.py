from rest_framework import serializers
from master import models as mst_models, serializers as mst_serializer

class OfficeDetailsSerializer(serializers.ModelSerializer):
    related_district =mst_serializer.DistrictSerializer(source="district", many=False, read_only=True)
    related_office_type =mst_serializer.OfficeTypeSerializer(source="office_type", many=False, read_only=True)
    class Meta:
        model = mst_models.OfficeDetails
        fields = (
            'id',
            'district',
            'office_type',
            'address',
            'pin',
            'is_deleted',
            'related_district',
            'related_office_type',
        )


