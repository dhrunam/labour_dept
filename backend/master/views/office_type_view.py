from rest_framework import generics, status, response
from master import models as mst_models, serializers as mst_serializer

class OfficeTypeList(generics.ListCreateAPIView):
    queryset = mst_models.OfficeType.objects.all().order_by("-id")
    serializer_class = mst_serializer.OfficeTypeSerializer


class OfficeTypeDetails(generics.RetrieveUpdateAPIView):
    queryset = mst_models.OfficeType
    serializer_class = mst_serializer.OfficeTypeSerializer