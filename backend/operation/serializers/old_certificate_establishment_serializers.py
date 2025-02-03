from rest_framework import serializers
from operation import models as op_models

class OldCertificateOfEstablishmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = op_models.OldCertificateOfEstablishment
        fields = "__all__"
