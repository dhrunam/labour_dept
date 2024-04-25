from rest_framework import generics, response, status, views
from django.contrib.auth.models import User, Group
from account import (models as acc_models, serializers as acc_serializer)
from master import (models as master_models)
from django.db import transaction, connection
from backend.utility import file_upload_handler
from django.contrib.auth import hashers
import re, json
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from durin.auth import TokenAuthentication
from django.db import models
from datetime import datetime, timedelta

def VerifyOTP(request, user):
    try:
        contact = request.data.get('contact')
        if contact:
            contact = re.sub('[^A-Za-z0-9]+', '', contact)
            
        otp = request.data.get('otp')
        if otp:
            otp = re.sub('[^A-Za-z0-9]+', '', otp)

        if user and otp:
            get_otp = acc_models.UserOTP.objects.filter(contact=contact).last()
            if get_otp:
                time_difference = datetime.now().astimezone() - get_otp.opt_date_time
                if time_difference >= timedelta(minutes=15):
                    return False
                if otp == get_otp.otp:
                       return True
                else:
                    return False
        
        else:
            return False

    except Exception as e:
        return False


class UserCreate(generics.CreateAPIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializerForRegistraion
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        try:

            request = file_upload_handler(self, request)
            print(request.data.get('group'))
            user = User.objects.create(
                        username=self.request.data.get('email'),
                        email=self.request.data.get('email'),
                        first_name=self.request.data.get('first_name'),
                        last_name=self.request.data.get('last_name'),
                        is_staff=True if self.request.data.get('group') == settings.USER_ROLES['general_user'] else False,
                    )
            user.groups.add(Group.objects.get(
                        name=self.request.data.get('group')))
            user.set_password(self.request.data.get('password'))
            user.save()

            user_profile = acc_models.UserProfile.objects.update_or_create(
                        user=user,
                        defaults={
                            # "name": request.data['name'],
                            "contact_number": request.data.get('contact_number'),
                            "email": request.data.get('email'),
                            "gender": request.data.get('gender', ''),
                            "document_type": request.data.get('document_type',''),
                            "id_proof": request.data.get('id_proof',''),
                            "organization": master_models.Organization.objects.get(pk=request.data.get('organization')) if  request.data.get('organization', False) else None,
                            "is_deleted": request.data.get('is_deleted'),
                        }
            )
            return response.Response("User created sucessfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return response.Response("Some error occured. Please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
        
class UserCreateFromAdmin(generics.CreateAPIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializerForRegistraion
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        request = file_upload_handler(self, request)
        user = User.objects.create(
                    username=self.request.data['username'],
                    is_staff=True if self.request.data['group'] == 'general_user' else False,
                )
        group_id_array=json.loads(self.request.data['group'])
        
        group_ids=list(Group.objects.filter(
               id__in=group_id_array).values_list('pk', flat=True))
        for item in group_ids:
             user.groups.add(item)
        user.set_password(self.request.data['password'])
        
        user.save()

        user_profile = acc_models.UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        # "name": request.data['name'],
                        "contact_number": request.data.get('contact_number'),
                        "email": request.data.get('email'),
                        "gender": request.data.get('gender', ''),
                        "document_type": request.data.get('document_type',''),
                        "id_proof": request.data.get('id_proof',''),
                        "organization": master_models.Organization.objects.get(pk=request.data.get('organization')) if  request.data.get('organization', False) else None,
                        "bar_registration_number": request.data.get('bar_registration_number',''),
                        "bar_certificate" : request.data.get('bar_certificate',''),
                        "is_deleted": request.data.get('is_deleted'),
                    }
        )
        return response.Response("User created sucessfully", status=status.HTTP_201_CREATED)
    
   
class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('-id')
    serializer_class = acc_serializer.UserSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes= (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
       # Use Subquery to filter users whose data is not available in UserProfile
        subquery = acc_models.UserProfile.objects.filter(user=models.OuterRef('pk'))
        
        return User.objects.annotate(has_profile=models.Exists(subquery)).filter(has_profile=True)


class UserRetrieve(generics.RetrieveAPIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class UserUpdate(generics.UpdateAPIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializerForRegistraion
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    user_roles=settings.USER_ROLES
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        user_name= self.request.user.username
        user_group = request.user.groups.all()
        
        if self.request.data.get('group'):
            group_id_array=json.loads(self.request.data.get('group'))
            
            group_ids=list(Group.objects.filter(
                id__in=group_id_array).values_list('pk', flat=True))
            # instance.groups.remove
            instance.groups.clear()
            for item in group_ids:
                group = Group.objects.get(id=item)
                
                instance.groups.add(group)
            instance.save()

        request.data._mutable = True
        # request= utility.file_upload_handler(self, request)
        if str(instance)==user_name or user_group.filter(name=self.user_roles['superadmin']).exists():
           
            super().put(request, *args, **kwargs)
        request.data._mutable = False
        return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        user_name= request.user.username
        user_group = request.user.groups.all()
        request.data._mutable = True
        if self.request.data.get('group'):
            group_id_array=json.loads(self.request.data.get('group'))
        
            group_ids=list(Group.objects.filter(
                id__in=group_id_array).values_list('pk', flat=True))
            # instance.groups.remove
            instance.groups.clear()
            for item in group_ids:
                group = Group.objects.get(id=item)
                instance.groups.add(group)
            instance.save()
       
      
        if str(instance)==user_name or  user_group.filter(name=self.user_roles['superadmin']).exists():
            
            super().patch(request, *args, **kwargs)
        request.data._mutable = False
        return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
    
    def get_object(self):
        return self.request.user
class UserUpdateByAdmin(generics.UpdateAPIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializerForRegistraion
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    user_roles=settings.USER_ROLES
    def put(self, request, *args, **kwargs):
        instance = self.get_object() 
        user_name= self.request.user.username
        user_group = self.request.user.groups.all()
        
        if self.request.data.get('group'):
            group_id_array=json.loads(self.request.data.get('group'))
            
            group_ids=list(Group.objects.filter(
                id__in=group_id_array).values_list('pk', flat=True))
            # instance.groups.remove
            instance.groups.clear()
            for item in group_ids:
                group = Group.objects.get(id=item)
                
                instance.groups.add(group)
            instance.save()

        request.data._mutable = True
        # request= utility.file_upload_handler(self, request)
        if str(instance)==user_name or user_group.filter(name=self.user_roles['superadmin']).exists():
           
            super().put(request, *args, **kwargs)
        request.data._mutable = False
        return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        user_name= request.user.username
        user_group = request.user.groups.all()
        request.data._mutable = True
        if self.request.data.get('group'):
            group_id_array=json.loads(self.request.data.get('group'))
        
            group_ids=list(Group.objects.filter(
                id__in=group_id_array).values_list('pk', flat=True))
            # instance.groups.remove
            instance.groups.clear()
            for item in group_ids:
                group = Group.objects.get(id=item)
                instance.groups.add(group)
            instance.save()
       
      
        if str(instance)==user_name or  user_group.filter(name=self.user_roles['superadmin']).exists():
            
            super().patch(request, *args, **kwargs)
        request.data._mutable = False
        return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
    
   

class UserForgotPasswordChange(views.APIView):
    queryset = User
    serializer_class = acc_serializer.UserSerializerForRegistraion
    
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        user = User.objects.filter(username=request.data.get('contact')).last()
        if user and VerifyOTP(request, user):
            user.set_password(request.data.get('password'))
            user.save()  
            return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
        request.data._mutable = False
        return response.Response("Password could not be changed", status=status.HTTP_403_FORBIDDEN)
    
    # def get_object(self):
    #     return self.request.user

