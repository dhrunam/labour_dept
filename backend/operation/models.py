from django.db import models
from master import models as mst_model
from django.conf import settings
from account import models as acc_models

# Create your models here.

class ApplicationForCertificateOfEstablishment(models.Model):
    office_location = models.ForeignKey(mst_model.District, on_delete = models.SET_NULL, null = True, related_name= "application_for_est")
    registration_status = models.CharField(max_length=128, null=False)
    full_name_applicant = models.CharField(max_length =256, null=False)
    email_applicant = models.CharField(max_length =256, null=False)
    photograph_applicant = models.FileField(upload_to='applicant/photograph/', null=True, blank=True)
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
    applied_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL, null=True, related_name="appl_for_certificate_est")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(auto_now=False)
    approved_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL,null=True, related_name="appr_for_certificate_est")

class ApplicationProgressHistory(models.Model):
    application_certificate_establishment = models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete=models.SET_NULL, null=True, related_name='application_progress_history')
    initiated_by = models.ForeignKey(acc_models.User, on_delete=models.SET_NULL, null=True, related_name="application_progress_history")
    remarks = models.CharField()
    application_status = models.CharField(max_length=128, null=False, default=settings.APPLICATION_STATUS["received"])
    created_at = models.DateTimeField(auto_now_add=True)

class EmployerParentageDetails(models.Model):
    application_certificate_establishment= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_parentel_details")
    parentage_name = models.CharField(max_length =256, null=False)
    designation = models.CharField(max_length =128, null=False)
    permanent_address = models.CharField(max_length =128, null=False)
    nature_interest = models.CharField(max_length =128, null=False)

class EmployerDetails(models.Model):
    application_certificate_establishment= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_details")
    name = models.CharField(max_length =128, null=False)
    designation =  models.CharField(max_length =128, null=False)
    permanent_address = models.CharField(max_length =512, null=False)

class EmployerFamilyMemberDetails(models.Model):
    application_certificate_establishment= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "employer_family_member")
    name = models.CharField(max_length =128, null=False)
    age =  models.DecimalField(max_digits=5, decimal_places=2 )
    gender = models.CharField(max_length =10, null=False)
    relationship = models.CharField(max_length =128, null=False)

class ManagementLevelEmployeeDetails(models.Model):
    application_certificate_establishment= models.ForeignKey(ApplicationForCertificateOfEstablishment, on_delete = models.SET_NULL, null= True, related_name = "management_level_employee")
    name = models.CharField(max_length =128, null=False)
    age =  models.DecimalField(max_digits=5, decimal_places=2 )
    gender = models.CharField(max_length =10, null=False)
    relationship = models.CharField(max_length =128, null=False)



