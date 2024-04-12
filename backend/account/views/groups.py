from rest_framework import generics
from django.contrib.auth.models import Group
from account.serializers import UserGroupSerializer
from rest_framework.permissions import IsAuthenticated
from durin.auth import TokenAuthentication
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie

# @method_decorator(csrf_protect, name='dispatch')
class GroupList(generics.ListAPIView):
    queryset = Group.objects.all().order_by('-id')
    serializer_class = UserGroupSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # @method_decorator(ensure_csrf_cookie)
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

# @method_decorator(csrf_protect, name='dispatch')
class GroupDetails(generics.RetrieveAPIView):
    queryset = Group
    serializer_class = UserGroupSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    # @method_decorator(ensure_csrf_cookie)
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)