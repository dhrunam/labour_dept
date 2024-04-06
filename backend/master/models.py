from django.db import models

# Create your models here.

class District(models.Model):
    district_name = models.CharField(max_length=128, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)

class OfficeType(models.Model):
    type=models.CharField(max_length=128, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)

class EstablishmentCategory(models.Model):
    category = models.CharField(max_length=512, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)

class OfficeDetails(models.Model):
    district = models.ForeignKey(District, default=None, null = True, on_delete= models.SET_NULL, related_name='office_details')
    office_type = models.ForeignKey(OfficeType, default= None, null=True, on_delete= models.SET_NULL, related_name='office_details')
    address = models.CharField(max_length=512, default=None, null=True)
    pin=models.CharField(max_length=512, default=None, null=True)
    is_deleted = models.BooleanField(default=False, null=False)