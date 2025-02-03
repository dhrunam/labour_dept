from rest_framework import  generics, response, status, views
from operation import models as op_models, serializers as op_serializer
from django.db import transaction, connection
from backend.utility import file_upload_handler
from django.conf  import settings
import json, datetime
from account import models as acc_models
from backend.utility import generate_application_no
from master import models as mst_models
from django.core.mail import send_mail

def ApplicationProgressHistoryInsert(self,data):
        op_models.ApplicationProgressHistory.objects.create(
            application = data['application'] ,
            initiated_by = self.request.user ,
            application_status = data['application_status'],
            remarks = data['remarks']
                
        )
class ApplicationForCertificateOfEstablishmentList(generics.ListCreateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer

    def get_queryset(self):

        # try:
        
        #     subject = 'Test'
        #     message = 'Hello'
        #     from_email = 'noreply.labour.'
        #     recipient_list = ['djb.sibin@gmail.com']
        #     send_mail(subject, message, from_email, recipient_list)

        # except Exception as e:
        #      print("Exceptions:", e)

        if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
           return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_by=self.request.user.id).order_by('-id')

        if self.request.user.groups.filter(name=settings.USER_ROLES["level1_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                return op_models.ApplicationForCertificateOfEstablishment.objects.filter(
                    applied_office_details=user_profile.organization).order_by('-id'
                                                                               )
        
        if self.request.user.groups.filter(name=settings.USER_ROLES["level2_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                return op_models.ApplicationForCertificateOfEstablishment.objects.filter(
                     applied_office_details=user_profile.organization).order_by('-id'
                                                                                        #  application_status=settings.APPLICATION_STATUS["t2-verification"]
                                                                                         )
        # if self.request.user.groups.filter(name=settings.USER_ROLES["level3_dept_admin"]).exists():
        #     user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
        #     if user_profile:

        #         # return op_models.ApplicationForCertificateOfEstablishment.objects.filter(applied_office_details=user_profile.organization,
        #         #                                                                          application_status=settings.APPLICATION_STATUS["t3-verification"]
        #         #                                                                          ).order_by('-id')
        #         return op_models.ApplicationForCertificateOfEstablishment.objects.all(
        #                                                                                 #  application_status=settings.APPLICATION_STATUS["t3-verification"]
        #                                                                                  ).order_by('-id')

        return []

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request = file_upload_handler(self,request)
        district = mst_models.District.objects.get(id=request.data.get('office_location'))
        application_number = generate_application_no(self, district.ref_no_prefix)
        request.data['application_no'] = application_number
        request.data['applied_by'] = self.request.user.id
        request.data['application_status'] = settings.APPLICATION_STATUS['received']
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        employer_parentage_details=json.loads(request.data.get('employer_parentage_details'))
        print('employer_parentage_details',employer_parentage_details)
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
        print('employer_details',employer_details)
        if employer_details and instance:
            for data in employer_details:
                op_models.EmployerDetails.objects.create(
                        application = instance,
                        name = data['name'],
                        designation = data['designation'],
                        permanent_address =data['permanent_address']

                )
        employer_family_member_details=json.loads(request.data.get('employer_family_member_details'))
        print('employer_family_member_details', employer_family_member_details)
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
        print('management_level_employee_details',management_level_employee_details)
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
                initiated_by = self.request.user ,
                application_status = settings.APPLICATION_STATUS["received"],
                remarks = self.request.data.get('remarks')

                
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
        if user_group.filter(name=self.user_roles['level2_dept_admin']).exists() and application_status == settings.APPLICATION_STATUS['approved']:
            request.data['approved_by'] = self.request.user.id
            request.data['approved_at'] = datetime.datetime.now()
        request.data._mutable = False
        return super().put(request, *args, **kwargs)
    
    @transaction.atomic()
    def patch(self, request, *args, **kwargs):
        request.data._mutable = True
        application_status = request.data.get('application_status')
        user_group = self.request.user.groups.all()
        print("remarks before:", request.data.get('remarks'))
        if user_group.filter(name=self.user_roles['general_user']).exists() :
            

            if application_status == settings.APPLICATION_STATUS['t1-verification']:
                new_data = {'application_status': application_status,
                            'remarks': request.data.get('remarks'),
                            }
                request._full_data = new_data


            if application_status == settings.APPLICATION_STATUS['t2-verification']:
                new_data = {'application_status': application_status,
                            'is_fee_deposited': True,
                            'token_number': request.data.get('token_number'),
                             'remarks': request.data.get('remarks'),
                            }
                request._full_data = new_data


        if user_group.filter(name=self.user_roles['level1_dept_admin']).exists() and application_status == settings.APPLICATION_STATUS['received']:
            new_data = {'application_status': settings.APPLICATION_STATUS['t1-verification']}
            if application_status == settings.APPLICATION_STATUS['received']:
                application_status=settings.APPLICATION_STATUS['t1-verification']
                new_data.update({
                    'calculated_fee': request.data.get('calculated_fee',0),
                    'token_number': '',
                    'remarks': request.data.get('remarks')
                })
                request._full_data = new_data

        
        if user_group.filter(name=self.user_roles['level2_dept_admin']).exists():
            new_data = {'application_status': application_status}
            new_data.update({
                    'application_status': application_status,
                    'approved_by': self.request.user.id,
                    'approved_at': datetime.datetime.now(),
                    'remarks': request.data.get('remarks')

            })
            request._full_data = new_data
                

        if application_status:
            print("remarks after:", request.data.get('remarks'))
            ApplicationProgressHistoryInsert(self,{'application':self.get_object(),
                                            'initiated_by':self.request.user,
                                            'remarks': request.data.get('remarks'),
                                            'application_status':application_status
                                            })
        # request.data._mutable = False
        return super().patch(request, *args, **kwargs)
    

class DasboardReportApi(views.APIView):

   def get(self, request, *args, **kwargs):
        queryset=op_models.ApplicationForCertificateOfEstablishment.objects.all().order_by('-id')
        total_old=0
        if self.request.user.groups.filter(name=settings.USER_ROLES["level1_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                queryset = queryset.filter(
                    applied_office_details=user_profile.organization)
                total_old= op_models.OldCertificateOfEstablishment.objects.all().count()
        
        if self.request.user.groups.filter(name=settings.USER_ROLES["level2_dept_admin"]).exists():
            user_profile=acc_models.UserProfile.objects.filter(user=self.request.user.id).last()
            if user_profile:
                queryset = queryset.filter(
                     applied_office_details=user_profile.organization)
                total_old= op_models.OldCertificateOfEstablishment.objects.all().count()
                
        if self.request.user.groups.filter(name=settings.USER_ROLES["general_user"]).exists():
                queryset = queryset.filter(applied_by=self.request.user.id)
                total_old= op_models.OldCertificateOfEstablishment.objects.filter(applied_by=self.request.user.id).count()
        

        total= queryset.count()
        total_new_application = queryset.filter(application_status = 
                                                                    settings.APPLICATION_STATUS["received"]).count()

        total_approved_application = queryset.filter(application_status = 
                                                                        settings.APPLICATION_STATUS["approved"]).count()
        total_rejected_application = queryset.filter(application_status = 
                                                                        settings.APPLICATION_STATUS["rejected"]).count()
    
      
        return response.Response({'total':total,
                                'new_application':total_new_application,
                                'approved_application':total_approved_application,
                                'rejected_application':total_rejected_application,
                                'total_old':total_old
                                }, status=status.HTTP_200_OK)

    

