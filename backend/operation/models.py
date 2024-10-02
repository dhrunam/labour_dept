from django.db import models
from master import models as mst_model
from django.conf import settings
from account import models as acc_models
from common import custom_model_fields_validator as field_validator
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

# Create your models here.

class ApplicationForCertificateOfEstablishment(models.Model):
    application_no= models.CharField(max_length=50, null=False)
    office_location = models.ForeignKey(mst_model.District, on_delete = models.SET_NULL, null = True, related_name= "application_for_est")
    registration_status = models.CharField(max_length=128, null=False)
    full_name_applicant = models.CharField(max_length =256, null=False)
    email_applicant = models.CharField(max_length =256, null=False)
    photograph_applicant = models.FileField(upload_to='applicant/photograph/',  null=True,  validators=[field_validator.FileExtensionValidator(['.jpg', '.jpeg', '.png', '.pdf']),
                                            field_validator.FileSizeValidator(10*1024*1024),
                                            field_validator.FileMimeTypeValidator(['image/jpeg', 'image/png', 'application/pdf'])])
    establishment_name = models.CharField(max_length =256, null=False)
    establishment_address = models.CharField(max_length =256, null=False)
    establishment_pincode = models.CharField(max_length =6, null=False)
    situation_of_other_premises = models.CharField(max_length =1024, null=False)
    establishment_category = models.ForeignKey(mst_model.EstablishmentCategory, on_delete = models.SET_NULL, null = True, related_name="application_for_est")
    nature_business = models.CharField(max_length = 1024, null = False)
    total_emplyee_male_18=models.IntegerField(default=0)
    total_emplyee_female_18=models.IntegerField(default=0)
    total_emplyee_other_18=models.IntegerField(default=0)

    total_emplyee_male_14 = models.IntegerField(default=0)
    total_emplyee_female_14 = models.IntegerField(default=0)
    total_emplyee_other_14 = models.IntegerField(default=0)
    weekly_holidays_name = models.CharField(max_length =256, null=False)
    is_agreed_terms_and_condition = models.BooleanField(default = False)
    application_status = models.CharField(max_length=128, null=False, default=settings.APPLICATION_STATUS["received"])
    applied_office_details = models.ForeignKey(mst_model.OfficeDetails, on_delete = models.SET_NULL, null=True, related_name="application_for_est")
    applied_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL, null=True, related_name="appl_for_certificate_est_applied_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(auto_now=False, null=True)
    approved_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL,null=True, related_name="appr_for_certificate_est_approved_by")
    pull_status = models.BooleanField(default=False)
    pulled_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL,null=True, related_name="appr_for_certificate_est_pulled_by")
    calculated_fee =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_fee_deposited = models.BooleanField(default=False)
    token_number = models.CharField(max_length=20, default='')
    trade_licence = models.FileField(upload_to='applicant/trade_licence/',  null=True,  validators=[field_validator.FileExtensionValidator(['.jpg', '.jpeg', '.png', '.pdf']),
                                            field_validator.FileSizeValidator(10*1024*1024),
                                            field_validator.FileMimeTypeValidator(['image/jpeg', 'image/png', 'application/pdf'])])
   

# Signal to handle file deletion when an instance is deleted
@receiver(post_delete, sender=ApplicationForCertificateOfEstablishment)
def delete_file_from_user_qualification_on_delete(sender, instance, **kwargs):
    if instance.photograph_applicant:
        if os.path.isfile(instance.photograph_applicant.path):
            os.remove(instance.photograph_applicant.path)
    if instance.trade_licence:
        if os.path.isfile(instance.trade_licence.path):
            os.remove(instance.trade_licence.path)

# Signal to handle old file deletion before saving a new one
@receiver(pre_save, sender=ApplicationForCertificateOfEstablishment)
def delete_old_file_from_user_qualificationon_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # If instance is new, nothing to do
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return  # If instance does not exist, nothing to do

    old_file = old_instance.certificate
    new_file = instance.certificate

    if old_file and old_file != new_file:  # Check if the file is different
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

    old_file = old_instance.marksheet
    new_file = instance.marksheet

    if old_file and old_file != new_file:  # Check if the file is different
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class ApplicationProgressHistory(models.Model):
    application = models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete=models.SET_NULL, null=True, related_name='application_progress_history')
    initiated_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL, null=True, related_name="application_progress_history")
    remarks = models.CharField(max_length=1024, default='',blank=True )
    application_status = models.CharField(max_length=128, null=False, default=settings.APPLICATION_STATUS["received"])
    created_at = models.DateTimeField(auto_now_add=True)

class EmployerParentageDetails(models.Model):
    application= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_parentel_details")
    parentage_name = models.CharField(max_length =256, null=False)
    designation = models.CharField(max_length =128, null=False)
    permanent_address = models.CharField(max_length =128, null=False)
    nature_interest = models.CharField(max_length =128, null=False)

class EmployerDetails(models.Model):
    application= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_details")
    name = models.CharField(max_length =128, null=False)
    designation =  models.CharField(max_length =128, null=False)
    permanent_address = models.CharField(max_length =512, null=False)

class EmployerFamilyMemberDetails(models.Model):
    application= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_family_member")
    name = models.CharField(max_length =128, null=False)
    age =  models.DecimalField(max_digits=5, decimal_places=2 )
    gender = models.CharField(max_length =10, null=False)
    relationship = models.CharField(max_length =128, null=False)

class ManagementLevelEmployeeDetails(models.Model):
    application= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "management_level_employee")
    name = models.CharField(max_length =128, null=False)
    age =  models.DecimalField(max_digits=5, decimal_places=2 )
    gender = models.CharField(max_length =10, null=False)
    relationship = models.CharField(max_length =128, null=False)

class ApplicationNumberSequence(models.Model):
    prefix = models.CharField(max_length=50, null=False)
    sequence = models.IntegerField(default=0)




