from rest_framework import serializers
from master import models as mst_models

class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = mst_models.District
        fields = (
            'id',
            'district_name',
            'short_name',
            'is_deleted',
            'ref_no_prefix',
        )
