from django.db import models

# Create your models here.

class District(models.Model):
    district_name = models.CharField(max_length=128, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    ref_no_prefix = models.CharField(max_length=30, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)
    def __str__(self) -> str:
        return self.district_name +f'({self.short_name})'

class OfficeType(models.Model):
    type=models.CharField(max_length=128, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.type +f'({self.short_name})'

class EstablishmentCategory(models.Model):
    category = models.CharField(max_length=512, default=None, null=False, unique=True)
    short_name = models.CharField(max_length=5, default=None, null=True, blank=True, unique=True)
    is_deleted = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return self.category +f'({self.short_name})'

class OfficeDetails(models.Model):
    office = models.CharField(max_length=512, default=None, null=True, unique=True)
    district = models.ForeignKey(District, default=None, null = True, on_delete= models.SET_NULL, related_name='office_details')
    office_type = models.ForeignKey(OfficeType, default= None, null=True, on_delete= models.SET_NULL, related_name='office_details')
    address = models.CharField(max_length=512, default=None, null=True)
    pin=models.CharField(max_length=512, default=None, null=True)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        return self.office+f'-{self.pin}'