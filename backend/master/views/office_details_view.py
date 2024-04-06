from rest_framework import generics, status, response
from master import models as mst_models, serializers as mst_serializer

class OfficeDetailsList(generics.ListCreateAPIView):
    queryset = mst_models.OfficeDetails.objects.all().order_by("-id")
    serializer_class = mst_serializer.OfficeDetailsSerializer


class OfficeDetailsDetails(generics.RetrieveUpdateAPIView):
    queryset = mst_models.OfficeDetails
    serializer_class = mst_serializer.OfficeDetailsSerializer