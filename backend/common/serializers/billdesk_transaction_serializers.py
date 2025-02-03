from rest_framework import serializers
from common import models as comm_models


class BillDeskOrderTransactionSerializers(serializers.ModelSerializer):

    class Meta:
        model = comm_models.PaymentTransaction
        fields = '__all_-'