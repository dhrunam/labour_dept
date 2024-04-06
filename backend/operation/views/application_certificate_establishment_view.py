from rest_framework import  generics
from operation import models as op_models, serializers as op_serializer

class ApplicationForCertificateOfEstablishmentList(generics.ListCreateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer


class ApplicationForCertificateOfEstablishmentDetails(generics.RetrieveUpdateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer