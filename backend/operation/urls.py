
from django.db import router
from django.urls import include, path
from rest_framework import routers
from operation import views as op_views

urlpatterns = [
    path('application/establishment/list', op_views.ApplicationForCertificateOfEstablishmentList.as_view()),
    path('application/establishment/<int:pk>', op_views.ApplicationForCertificateOfEstablishmentDetails.as_view())
]
<<<<<<< HEAD
=======

>>>>>>> 891417f2d21530f48b47c7dbdd8fe79e772425bd
