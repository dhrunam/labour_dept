
from django.db import router
from django.urls import include, path
from rest_framework import routers
from common import views as comm_views

urlpatterns = [
    # path('application/online_payment/initiate', comm_views.PaymentDetailList.as_view()),
    path('application/online_payment/initiate', comm_views.InitiatePaymentAPIView.as_view()),
    # path('application/online_payment/fake', comm_views.FakePaymentGateWayRequest.as_view()),

    # path('application/online_payment/callbak', comm_views.PaymentResponseHandler.as_view()),
    path('application/online_payment/callback', comm_views.BillDeskCallbackAPIView.as_view()),
    
]
