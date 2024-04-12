from master import models as master_models
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=128, default=None, null=False)
    contact_number = models.CharField(max_length=10, default=None, null=False)
    email = models.CharField(max_length=128, default=None, null=False)
    gender = models.CharField(max_length=16, default=None, null=True)
    document_type = models.CharField(max_length=128, default=None, null=True)
    id_proof = models.FileField(upload_to='id_proofs/{}'.format(datetime.datetime.now().year), null=True, blank=True)
    organization = models.ForeignKey(master_models.OfficeDetails, on_delete=models.CASCADE, null=True)
    is_deleted = models.BooleanField(default=None, null=False)

class UserOTP(models.Model):
    contact = models.CharField(max_length=50, default=None, null=False, unique=True)
    otp = models.CharField(max_length=6, default=None, null=False)