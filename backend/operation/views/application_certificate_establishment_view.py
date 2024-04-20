from rest_framework import  generics, response, status
from operation import models as op_models, serializers as op_serializer
from django.db import transaction, connection
from backend.utility import file_upload_handler
from django.conf  import settings
import json, datetime


class ApplicationForCertificateOfEstablishmentList(generics.ListCreateAPIView):
    queryset = op_models.ApplicationForCertificateOfEstablishment.objects.all().order_by('-id')
    serializer_class = op_serializer.ApplicationForCertificateOfEstablishmentSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request = file_upload_handler(self,request)
        request.data['applied_by'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        


        employer_parentage_details=json.loads(request.data.get('employer_parentage_details'))
        if employer_parentage_details and instance:
            for data in employer_parentage_details:
                op_models.EmployerParentageDetails.objects.create(
                        application_certificate_establishment = instance,
                        parentage_name = data['parentage_name'],
                        designation = data['designation'],
                        permanent_address =data['permanent_address'],
                        nature_interest = data['nature_interest']
                )
        employer_details=json.loads(request.data.get('employer_details'))
        if employer_details and instance:
            for data in employer_details:
                op_models.EmployerDetails.objects.create(
                        application_certificate_establishment = instance,
                        name = data['name'],
                        designation = data['designation'],
                        permanent_address =data['permanent_address']

                )
        employer_family_member_details=json.loads(request.data.get('employer_family_member_details'))
        if employer_family_member_details and instance:
            for data in employer_family_member_details:
                op_models.EmployerFamilyMemberDetails.objects.create(
                        application_certificate_establishment = instance,
                        name = data['name'],
                        age = data['age'],
                        gender = data['gender'],
                        relationship =data['relationship']

                )
        management_level_employee_details=json.loads(request.data.get('management_level_employee_details'))
        if management_level_employee_details and instance:
            for data in management_level_employee_details:
                op_models.ManagementLevelEmployeeDetails.objects.create(
                        application_certificate_establishment = instance,
                        name = data['name'],
                        age = data['age'],
                        gender = data['gender'],
                        relationship =data['relationship']

                )
        
        op_models.ApplicationProgressHistory.objects.create(
                application_certificate_establishment = instance,
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
        if user_group.filter(name=self.user_roles['dept_admin']).exists() and application_status == settings.APPLICATION_STATUS['approved']:
            request.data['approved_by'] = self.request.user.id
            request.data['approved_at'] = datetime.datetime.now()
        request.data._mutable = False
        return super().put(request, *args, **kwargs)