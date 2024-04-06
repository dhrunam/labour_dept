from rest_framework import serializers
from operation import models as op_models, serializers as op_serializer
from master import serializers as mst_serializers


class ApplicationForCertificateOfEstablishmentSerializer(serializers.ModelSerializer):
    related_office_situated_at = mst_serializers.DistrictSerializer(source='office_location', many=False, read_only = True)
    related_establishment_category = mst_serializers.EstablishmentCategorySerializer(source='establishment_category', many=False, read_only=True)
    related_applied_office_details = mst_serializers.OfficeDetailsSerializer(source='applied_office_details', many=False, read_only=True)
     
    related_employer_parentage_details = op_serializer.EmployerParentageDetailsSerializer(source='employer_parentel_details', many=True, read_only=True)

    related_employer_details = op_serializer.EmployerDetailsSerializer(source = 'employer_details',many=True, read_only=True)

    related_employer_family_member_details = op_serializer.EmployerFamilyMemberDetailsSerializer(source = 'employer_family_member',many=True, read_only=True)

    related_management_level_employee_details = op_serializer.ManagementLevelEmployeeDetailsSerializer(source = 'management_level_employee',many=True, read_only=True)
     
    class Meta:
          model = op_models.ApplicationForCertificateOfEstablishment
          fields = (
                    'id',
                    'office_location',
                    'registration_status',
                    'full_name_applicant',
                    'email_applicant',
                    'photograph_applicant',
                    'establishment_name',
                    'establishment_address',
                    'establishment_pincode',
                    'situation_of_other_premises',
                    'establishment_category',
                    'nature_business',
                    'total_emplyee_male_18',
                    'total_emplyee_female_18',
                    'total_emplyee_other_18',
                    'total_emplyee_male_14',
                    'total_emplyee_female_14',
                    'total_emplyee_other_14',
                    'weekly_holidays_name',
                    'is_agreed_terms_and_condition',
                    'applied_office_details',
                    'related_office_situated_at',
                    'related_establishment_category',
                    'related_applied_office_details',
                    'related_employer_parentage_details',
                    'related_employer_details',
                    'related_employer_family_member_details',
                    'related_management_level_employee_details',

                    )


