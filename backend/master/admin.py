from django.contrib import admin
from master import models as mst_models


# Register your models here.

admin.site.register([mst_models.District,mst_models.EstablishmentCategory,mst_models.OfficeType, mst_models.OfficeDetails])

