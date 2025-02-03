from rest_framework import generics, status, response
from master import models as mst_models, serializers as mst_serializer

class OfficeDetailsList(generics.ListCreateAPIView):
    queryset = mst_models.OfficeDetails.objects.all().order_by("-id")
    serializer_class = mst_serializer.OfficeDetailsSerializer

   

    def get_queryset(self):
        queryset = mst_models.OfficeDetails.objects.all().order_by("-id")
        district = self.request.query_params.get('district')
        if district is not None:
            queryset=queryset.filter(district=district)
        return queryset


class OfficeDetailsDetails(generics.RetrieveUpdateAPIView):
    queryset = mst_models.OfficeDetails
    serializer_class = mst_serializer.OfficeDetailsSerializer