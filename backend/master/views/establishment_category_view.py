from rest_framework import generics, status, response
from master import models as mst_models, serializers as mst_serializer

class EstablishmentCategoryList(generics.ListCreateAPIView):
    queryset = mst_models.EstablishmentCategory.objects.all().order_by("-id")
    serializer_class = mst_serializer.EstablishmentCategorySerializer


class EstablishmentCategoryDetails(generics.RetrieveUpdateAPIView):
    queryset = mst_models.EstablishmentCategory
    serializer_class = mst_serializer.EstablishmentCategorySerializer