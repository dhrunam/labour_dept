from account import (models as acc_models, serializers as acc_serializers)
from rest_framework import generics, response,status
from django.db import transaction, connection
from django.contrib.auth.models import User
import requests, random, re
from datetime import datetime, timedelta
from backend.utility import send_sms, send_emil_from_app

from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie

def GenerateSendOTP( contact, otp_for ):
    sent = False
    otp = random.randint(100000,999999)

    check = acc_models.UserOTP.objects.filter(contact = contact).last()
    if check:
        check.otp = otp
        check.save()
    else:
        acc_models.UserOTP.objects.create(
            contact = contact,
            otp = otp
        )
    if otp_for=="phone_number":
            send_sms(contact,'1107165390653742984','Hello, OTP for phone verification is '+str(otp)+' advtent-High Court of Sikkim')
            sent =True
    if otp_for=="email":
            send_emil_from_app(contact,'1107165390653742984','Hello, OTP for phone verification is '+str(otp)+' advtent-High Court of Sikkim')
            sent = True
    
    return sent

def VerifyEmailOTPForUserRegistration(contact, otp, user_type):
    check = User.objects.filter(username=contact).last()
    if(check):
        acc_models.UserOTP.objects.filter(contact=contact).delete()
        return False
    else:
        get_otp = acc_models.UserOTP.objects.filter(contact=contact).last()
        if get_otp:
            time_difference = datetime.now().astimezone() - get_otp.opt_date_time
            if time_difference >= timedelta(minutes=15):
                return False
            if otp == get_otp.otp:
                get_otp.delete()
                return True
                    
            else:
                return False
        else:
            return False

def VerifyPhoneNumberOTPForUserRegistration(contact, otp):
        get_otp = acc_models.UserOTP.objects.filter(contact=contact).last()
        if get_otp:
            time_difference = datetime.now().astimezone() - get_otp.opt_date_time
            if time_difference >= timedelta(minutes=15):
                return response.Response("OTP Expired", status=status.HTTP_400_BAD_REQUEST)
            if otp == get_otp.otp:
                get_otp.delete()
                return True
                    
            else:
                return False
        else:
            return False


# @method_decorator(csrf_protect, name='dispatch')
class UserOtpList(generics.ListCreateAPIView):

    queryset = acc_models.UserOTP
    serializer_class = acc_serializers.UserOTPSerializer

    def post(self, request, *args, **kwargs):
        phone_otp_verification = False
        email_otp_verification = False
        sent_email_otp = False
        sent_phone_otp = False
        try:
            contact = request.data.get('contact')
            email = request.data.get('email')
            if contact:
                contact = re.sub('[^0-9]+', '', contact)
            else:
                return response.Response("Contact number required.", status=status.HTTP_404_NOT_FOUND)

            otp = request.data.get('otp')
            if otp:
                 otp = re.sub('[^0-9]+', '', otp)
            elif contact:
                sent_phone_otp = GenerateSendOTP(contact,'phone_number')
            elif email:
                sent_email_otp = GenerateSendOTP(email,'email')
            
            if sent_phone_otp:
                return response.Response("Otp send successfully to phone number..", status==status.HTTP_200_OK)
            if sent_email_otp:
                return response.Response("Otp send successfully to email..", status==status.HTTP_200_OK)
           
            if contact and otp:
               
                phone_otp_verification = VerifyPhoneNumberOTPForUserRegistration(contact,otp)

            if email and otp:
                email_otp_verification = VerifyEmailOTPForUserRegistration(email,otp)
            
            if phone_otp_verification and email_otp_verification:
                
                return response.Response("Otp varified successfully", status==status.HTTP_200_OK)
            

        except Exception as e:
         
            return response.Response("Some error occured. Please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @method_decorator(ensure_csrf_cookie)
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

        
    
    # def get(self, request, *args, **kwargs):
       
    #     try:
    #         contact = re.sub('[^A-Za-z0-9]+', '', request.query_params.get('contact'))
    #         otp = re.sub('[^A-Za-z0-9]+','', request.query_params.get('otp'))
    #         user_type = re.sub('[^A-Za-z0-9]+', '', request.query_params.get('user'))
            
                    
    #     except Exception as e:
           
    #         return response.Response("Incorrect OTP or OTP expired..", status=status.HTTP_403_FORBIDDEN)

# @method_decorator(csrf_protect, name='dispatch')
class OtpForForgetPassword(generics.ListCreateAPIView):
    queryset = acc_models.UserOTP
    serializer_class = acc_serializers.UserOTPSerializer

    def post(self, request, *args, **kwargs):
       
       
        try:
            contact = request.data.get('contact')
            if contact:
                contact = re.sub('[^A-Za-z0-9]+', '', contact)
            else:
                return response.Response("Contact number required.", status=status.HTTP_404_NOT_FOUND)

            check = User.objects.filter(username=contact).last()
            
            otp = request.data.get('otp')
            if otp:
                 otp = re.sub('[^A-Za-z0-9]+', '', otp)
            else:
                if check:
                    return GenerateSendOTP(contact)
                else :
                    return response.Response("User does not exist.", status=status.HTTP_403_FORBIDDEN)

        
            if check and otp:
                get_otp = acc_models.UserOTP.objects.filter(contact=contact).last()
                if get_otp:
                    time_difference = datetime.now().astimezone() - get_otp.opt_date_time
                    if time_difference >= timedelta(minutes=15):
                        return response.Response("OTP Expired", status=status.HTTP_400_BAD_REQUEST)
                    if otp == get_otp.otp:
                       return response.Response("OTP Verified", status=status.HTTP_200_OK)
                    else:
                        return response.Response("OTP mismatch", status=status.HTTP_403_FORBIDDEN)
                else:
                    return response.Response("OTP does not exist.", status=status.HTTP_403_FORBIDDEN)
        
            else:
                return response.Response("User or OTP could not find.", status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
           
            return response.Response("Some error occured. Please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @method_decorator(ensure_csrf_cookie)
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)