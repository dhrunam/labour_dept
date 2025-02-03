from rest_framework import  generics, response, status
from operation import models as op_models, serializers as op_serializer
from django.db import transaction, connection
from backend.utility import file_upload_handler
from django.conf  import settings
import json, datetime
from account import models as acc_models
from backend.utility import generate_application_no
from master import models as mst_models

class OldCertificateOfEstablishmentList(generics.ListAPIView):

    queryset = op_models.OldCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.OldCertificateOfEstablishmentSerializers

    def get_queryset(self):
        
        queryset = op_models.OldCertificateOfEstablishment.objects.all().order_by('-id')
        
        old_registration_number = self.request.query_params.get('search_text')

       
        # if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
        #    return queryset.filter(applied_by=self.request.user.id).order_by('-id')

        # if self.request.user.groups.filter(name=settings.USER_ROLES["level1_dept_admin"]).exists():
        #     user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
        #     if user_profile:
        #         return queryset.filter(
        #             applied_office_details=user_profile.organization).order_by('-id'
        #                                                                        )
        
        # if self.request.user.groups.filter(name=settings.USER_ROLES["level2_dept_admin"]).exists():
        #     user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
        #     if user_profile:
        #         return queryset.filter(
        #              applied_office_details=user_profile.organization).order_by('-id')

        if old_registration_number:
            return queryset.filter(registration_number__icontains=old_registration_number)
        else:
            if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
                print('User-id:', self.request.user.id)
                return queryset.filter(applied_by=self.request.user.id).order_by('-id')

            if self.request.user.groups.filter(name=settings.USER_ROLES["level1_dept_admin"]).exists():
                user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
                if user_profile:
                    return queryset.filter(
                        applied_office_details=user_profile.organization).order_by('-id'
                                                                                )
            
            if self.request.user.groups.filter(name=settings.USER_ROLES["level2_dept_admin"]).exists():
                user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
                if user_profile:
                    return queryset.filter(
                        applied_office_details=user_profile.organization).order_by('-id')



        
        return queryset
      
class OldCertifcateOfEstablishmentDetails(generics.RetrieveUpdateAPIView):
    queryset = op_models.OldCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.OldCertificateOfEstablishmentSerializers

    def patch(self, request, *args, **kwargs):
        request.data._mutable = True
        request = file_upload_handler(self,request)
        if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
            request.data['applied_by']= self.request.user.id
            request.data['updated_by']= self.request.user.id

        if self.request.user.groups.filter(name=settings.USER_ROLES["level1_dept_admin"]).exists():
            request.data['approved_by']= self.request.user.id
            request.data['updated_by']= self.request.user.id
            request.data['approved_at']= datetime.datetime.now()

            
        if self.request.user.groups.filter(name=settings.USER_ROLES["level2_dept_admin"]).exists():
            request.data['approved_by']= self.request.user.id
            request.data['updated_by']= self.request.user.id
            request.data['approved_at']= datetime.datetime.now()
               
        return super().patch(request, *args, **kwargs)

