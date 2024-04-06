from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from account.views import 

urlpatterns = [
     path('auth/',include('durin.urls')),
]
