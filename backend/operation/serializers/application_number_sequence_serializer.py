from rest_framework import serializers
from operation import models as op_models
class ApplicationNumberSequenceSerializer(serializers.ModelSerializer):

    class meta:
        model = op_models.ApplicationNumberSequence
        fields =(
            'id',
            'application_no',
            'district',
        )