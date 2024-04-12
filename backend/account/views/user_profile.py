from rest_framework import generics,status, response
from account import models as acc_models, serializers as acc_serializers
from django.conf import settings
from backend.utility import file_upload_handler
from rest_framework.permissions import IsAuthenticated
from durin.auth import TokenAuthentication
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import (csrf_protect, ensure_csrf_cookie, csrf_exempt)



@method_decorator(csrf_protect, name='dispatch')
class UserProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = acc_models.UserProfile
    serializer_class = acc_serializers.UserProfileSerializer
    user_roles=settings.USER_ROLES
    authentication_classes = (TokenAuthentication,)
    permission_classes =(IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_name= request.user.username
            user_group = request.user.groups.all()

            request.data._mutable = True
        
            if user_group.filter(name=self.user_roles['superadmin']).exists() or str(instance)==user_name:
                request= file_upload_handler(self, request)
            super().put(request, *args, **kwargs)
            request.data._mutable = False
            return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response("Some error occured. Please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def patch(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            user_name= request.user.username
            user_group = request.user.groups.all()

            request.data._mutable = True
            if user_group.filter(name=self.user_roles['superadmin']).exists() or str(instance)==user_name:
                request= file_upload_handler(self, request)
            super().patch(request, *args, **kwargs)
            request.data._mutable = False

            return response.Response("Updated successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response("Some error occured. Please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # @method_decorator(ensure_csrf_cookie)
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
