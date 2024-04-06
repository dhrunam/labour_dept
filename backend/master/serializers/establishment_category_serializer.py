from rest_framework import serializers
from master import models as mst_models

class EstablishmentCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = mst_models.EstablishmentCategory
        fields = (
            'category',
            'short_name',
            'is_deleted'
        )
