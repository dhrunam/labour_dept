from rest_framework import generics, status, response
from master import models as mst_models, serializers as mst_serializer

class DistrictList(generics.ListCreateAPIView):
    queryset = mst_models.District.objects.all().order_by('-id')
    serializer_class = mst_serializer.DistrictSerializer



class DistrictDetails(generics.RetrieveUpdateAPIView):
    queryset = mst_models.District
    serializer_class = mst_serializer.DistrictSerializer

    