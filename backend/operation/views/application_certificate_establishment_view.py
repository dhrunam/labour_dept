from rest_framework import  generics, response, status
from operation import models as op_models, serializers as op_serializer
from django.db import transaction, connection
from backend.utility import file_upload_handler
from django.conf  import settings
import json, datetime
from account import models as acc_models
from backend import utility


def ApplicationProgressHistoryInsert(self,data):
        op_models.ApplicationProgressHistory.objects.create(
            application = data['application'] ,
            initiated_by = self.request.user ,
            application_status = settings.APPLICATION_STATUS["received"],

                
        )
class ApplicationForCertificateOfEstablishmentList(generics.ListCreateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer

    def get_queryset(self):
        
            
        if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
           return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_by=self.request.user.id).order_by('-id')

        if self.request.user.groups.filter(name=settings.USER_ROLES["levl1_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_office_details=user_profile.organization).order_by('-id')
        
        if self.request.user.groups.filter(name=settings.USER_ROLES["levl2_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_office_details=user_profile.organization,
                                                                                         application_status=settings.APPLICATION_STATUS["t2-verification"]
                                                                                         ).order_by('-id')
        if self.request.user.groups.filter(name=settings.USER_ROLES["levl3_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_office_details=user_profile.organization,
                                                                                         application_status=settings.APPLICATION_STATUS["t3-verification"]
                                                                                         ).order_by('-id')

        return []

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request = file_upload_handler(self,request)
        application_number = utility.generate_application_no(self, request.data.get('application_no_prefix'))
        request.data['application_no'] = application_number
        request.data['applied_by'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        employer_parentage_details=json.loads(request.data.get('employer_parentage_details'))

        if employer_parentage_details and instance:
            for data in employer_parentage_details:
                op_models.EmployerParentageDetails.objects.create(
                        application = instance,
                        parentage_name = data['parentage_name'],
                        designation = data['designation'],
                        permanent_address =data['permanent_address'],
                        nature_interest = data['nature_interest']
                )
        employer_details=json.loads(request.data.get('employer_details'))
        if employer_details and instance:
            for data in employer_details:
                op_models.EmployerDetails.objects.create(
                        application = instance,
                        name = data['name'],
                        designation = data['designation'],
                        permanent_address =data['permanent_address']

                )
        employer_family_member_details=json.loads(request.data.get('employer_family_member_details'))
        if employer_family_member_details and instance:
            for data in employer_family_member_details:
                op_models.EmployerFamilyMemberDetails.objects.create(
                        application= instance,
                        name = data['name'],
                        age = data['age'],
                        gender = data['gender'],
                        relationship =data['relationship']

                )
        management_level_employee_details=json.loads(request.data.get('management_level_employee_details'))
        if management_level_employee_details and instance:
            for data in management_level_employee_details:
                op_models.ManagementLevelEmployeeDetails.objects.create(
                        application = instance,
                        name = data['name'],
                        age = data['age'],
                        gender = data['gender'],
                        relationship =data['relationship']

                )
        
        op_models.ApplicationProgressHistory.objects.create(
                application = instance,
                # initiated_by = self.request.user ,
                application_status = settings.APPLICATION_STATUS["received"],

                
        )
        
        request.data._mutable = False

        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ApplicationForCertificateOfEstablishmentDetails(generics.RetrieveUpdateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer
    user_roles=settings.USER_ROLES
    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        application_status = request.data.get('application_status')
        user_group = self.request.user.groups.all()
        if user_group.filter(name=self.user_roles['levl3_dept_admin']).exists() and application_status == settings.APPLICATION_STATUS['approved']:
            request.data['approved_by'] = self.request.user.id
            request.data['approved_at'] = datetime.datetime.now()
        request.data._mutable = False
        return super().put(request, *args, **kwargs)
    
    @transaction.atomic()
    def patch(self, request, *args, **kwargs):

        request.data._mutable = True
        application_status = request.data.get('application_status')
        user_group = self.request.user.groups.all()
        if user_group.filter(name=self.user_roles['levl1_dept_admin']).exists() :
            

            if application_status == settings.APPLICATION_STATUS['t2-verification']:
                new_data = {'application_status': application_status
                            }
                request._full_data = new_data


            if application_status == settings.APPLICATION_STATUS['t3-verification']:
                new_data = {'application_status': application_status,
                            'is_fee_deposited': True,
                            'token_number': request.data.get('token_number')
                            }
                request._full_data = new_data


        if user_group.filter(name=self.user_roles['levl2_dept_admin']).exists() and application_status == settings.APPLICATION_STATUS['t3-verification']:
            new_data = {'application_status': application_status}
            if application_status == settings.APPLICATION_STATUS['t1-verification']:
                new_data.update({
                    'calculated_fee': request.data.get('calculated_fee',0)

                })
                request._full_data = new_data

        
        if user_group.filter(name=self.user_roles['levl3_dept_admin']).exists():
            if application_status == settings.APPLICATION_STATUS['approved']:
                new_data.update({
                    'application_status': application_status,
                    'approved_by': self.request.user.id,
                    'approved_at': datetime.datetime.now()

                })
                request._full_data = new_data

        if application_status:
            ApplicationProgressHistoryInsert(self,{'application':self.get_object(),
                                            'initiated_by':self.request.user,
                                            'remarks': request.data.get('remarks'),
                                            'application_status':application_status
                                            })
        request.data._mutable = False
        return super().put(request, *args, **kwargs)
    
    