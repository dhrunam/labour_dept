from rest_framework import generics, status, response, views
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
import random
import string
import json
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.permissions import IsAuthenticated, AllowAny

from common import models as comm_models, serializers as comm_serializers
from backend.utility import (   generate_jws_v2, 
                                generate_application_no,
                                get_auth_token,
                                generate_hmac_sha256_checksum,
                               )


import json
import time
import requests
import hashlib
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from common.models import PaymentTransaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from operation import models as op_models


BILLDESK_URL = settings.PG_PARAMS['payment_request_url']

class InitiatePaymentAPIView(APIView):
    """
    Step 1: Initiates Payment and Sends Request to BillDesk as a 'msg' parameter
    """

    def post(self, request):
        data = request.data
        user = request.user

        # Generate unique Order ID
        order_id = f"ORD-{user.id}-{int(time.time())}"

        # Create a new payment transaction
        payment_transaction = PaymentTransaction.objects.create(
            application = request.data.get('application'),
            application_no = request.data.get('application_no'),
            application_generation = request.data.get('application_generation'),
            merchant_id=settings.PG_PARAMS['merchant_code'],
            security_id=settings.PG_PARAMS['client_id'],
            security_password=data.get('security_password'),
            security_type=data.get('security_type'),
            order_id=order_id,
            amount=data.get('amount'),
            currency_name=data.get('currency_name', 'INR'),
            txn_type=data.get('txn_type', ''),
            additional_info1=data.get('additional_info1', 'NA'),
            additional_info2=data.get('additional_info2', 'NA'),
            additional_info3=data.get('additional_info3', 'NA'),
            additional_info4=data.get('additional_info4', 'NA'),
            additional_info5=data.get('additional_info5', 'NA'),
            additional_info6=data.get('additional_info6', 'NA'),
            additional_info7=data.get('additional_info7', 'NA'),
            created_by = user,
        )
        # Create pipe-separated "msg" string
        #     Request:
        #   MerchantID | CustomerID | 
        #   NA | TxnAmount |    
        #   NA | NA | NA | 
        #   CurrencyType | NA | TypeFieId1 | 
        #   SecurityID | NA | NA | 
        #   TypeField2 | txtadditional1 | txtadditional2 | 
        #   txtadditional3 | txtadditional4 | txtadditional5 |
        #   txtadditional6 | txtadditional7 | RU
        raw_string = f"{payment_transaction.merchant_id}|{payment_transaction.order_id}|"\
                     f"{payment_transaction.na1}|{payment_transaction.amount}|"\
                     f"{payment_transaction.na2}|{payment_transaction.na3}|{payment_transaction.na4}|"\
                     f"{payment_transaction.currency_name}|{payment_transaction.na5}|{payment_transaction.type_field1}|"\
                     f"{payment_transaction.security_id}|{payment_transaction.na6}|{payment_transaction.na7}|"\
                     f"{payment_transaction.type_field2}|{payment_transaction.additional_info1}|{payment_transaction.additional_info2}|"\
                     f"{payment_transaction.additional_info3}|{payment_transaction.additional_info4}|{payment_transaction.additional_info5}|"\
                     f"{payment_transaction.additional_info6}|{payment_transaction.additional_info7}|{settings.PG_PARAMS['return_url']}"
        
        # Generate checksum
        payment_transaction.checksum = payment_transaction.generate_checksum(raw_string)
        payment_transaction.save()

       

        msg = f"{raw_string}|{payment_transaction.checksum}"
        # Prepare payload for BillDesk (as required)
        payload = {
            "msg": msg  # BillDesk expects a single "msg" field with pipe-separated values
        }

        print("Msg:", msg)

         # Render an HTML form and auto-submit it
        html_form = f"""
        <html>
        <body onload="document.forms['billdesk_form'].submit();">
            <form name="billdesk_form" method="post" action="{BILLDESK_URL}">
                <input type="hidden" name="msg" value="{msg}" />
            </form>
            <p>Redirecting to BillDesk...</p>
        </body>
        </html>
        """
        
        # return HttpResponse(html_form)

        # Send payment request to BillDesk
        print("Billdesk URL", BILLDESK_URL + msg)
        response = requests.get(BILLDESK_URL)

        # Store response data
        payment_transaction.response_payload = response.text
        payment_transaction.save()

        return Response({
            "message": "Payment initiated",
            "order_id": payment_transaction.order_id,
            "msg": msg,
            "url": BILLDESK_URL
        }, status=status.HTTP_201_CREATED)




class BillDeskCallbackAPIView(APIView):
    """
    Step 2: Handles BillDesk Payment Response and Updates Database
    """

    @csrf_exempt
    def post(self, request):
        try:
            print("Inside Try...")
            response_data = request.data.get('msg','Not found..')
            print("response_data:", response_data)
            # Extract pipe-separated "msg" parameter
            msg = response_data
            print("msg:", msg)
           # Split the message using the pipe separator and strip any extra spaces
            msg_parts = [part.strip() for part in msg.split("|")]
            print("msg_parts:", msg_parts)
            # Assigning each field to a separate variable
            merchant_id = msg_parts[0]
            order_id = msg_parts[1]
            txn_reference_no = msg_parts[2]
            bank_reference_no = msg_parts[3]
            txn_amount = msg_parts[4]
            ibank_id = msg_parts[5]
            bank_merchant_id = msg_parts[6]
            txn_type = msg_parts[7]
            currency_name = msg_parts[8]
            item_code = msg_parts[9]
            security_type = msg_parts[10]
            security_id = msg_parts[11]
            security_password = msg_parts[12]
            txn_date = msg_parts[13]
            auth_status = msg_parts[14]
            settlement_type = msg_parts[15]
            additional_info1 = msg_parts[16]
            additional_info2 = msg_parts[17]
            additional_info3 = msg_parts[18]
            additional_info4 = msg_parts[19]
            additional_info5 = msg_parts[20]
            additional_info6 = msg_parts[21]
            additional_info7 = msg_parts[22]
            error_status = msg_parts[23]
            error_description = msg_parts[24]
            checksum = msg_parts[25]
            print("Check_Sum", checksum)
            # Retrieve related payment request
            payment_transaction = PaymentTransaction.objects.get(order_id=order_id)

            # Update Payment Transaction record
            payment_transaction.txn_reference_no = txn_reference_no
            payment_transaction.bank_reference_no = bank_reference_no
            payment_transaction.auth_status = auth_status
        
            payment_transaction.response_payload = json.dumps(response_data)
            # payment_transaction.checksum = checksum

            payment_transaction.error_status = error_status
            payment_transaction.error_description = error_description
            payment_transaction.security_id= security_id
            payment_transaction.security_type = security_type
            payment_transaction.security_password = security_password

            # Verify checksum
            if not payment_transaction.verify_checksum(msg):
                return JsonResponse({"error": "Checksum verification failed"}, status=400)

            # Update payment transaction status
            payment_transaction.status =  'SUCCESS' if auth_status=='0300' else 'FAILED'
            payment_transaction.save()

            if auth_status=='0300':
                op_models.ApplicationForCertificateOfEstablishment.objects.filter(
                    id= payment_transaction.application
                    ).update(
                        application_status= settings.APPLICATION_STATUS['fee_payment_success'],
                        is_fee_deposited = True,
                        token_number = txn_reference_no,
                     
                    )
                
                
                op_models.ApplicationProgressHistory.objects.create(
                application =op_models.ApplicationForCertificateOfEstablishment.objects.get(id=payment_transaction.application) ,
                initiated_by = payment_transaction.created_by ,
                application_status = settings.APPLICATION_STATUS['fee_payment_success'],
                remarks = 'Online fee payment success by user.'
                
                )
                frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_success']+"?msg=" + msg
                return HttpResponseRedirect(frontend_url)
            else:
                frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_fail']+"?msg=" + msg
                return HttpResponseRedirect(frontend_url)
            # return JsonResponse({"message": "Payment status updated successfully"}, status=200)

        except PaymentTransaction.DoesNotExist:
            # return JsonResponse({"error": "Order not found"}, status=404)
            if auth_status=='0300':
                frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_success']+"?msg=" + msg
                return HttpResponseRedirect(frontend_url)
            frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_fail']+"?msg=" + msg
            return HttpResponseRedirect(frontend_url)

        except Exception as e:
            # return JsonResponse({"error": str(e)}, status=500)
            if auth_status=='0300':
                frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_success']+"?msg=" + msg
                return HttpResponseRedirect(frontend_url)
           
            frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_fail']+"?msg=" + msg
            return HttpResponseRedirect(frontend_url)



def get_request_msg_with_checksum(request):
    print('Merchant_1:' )
    msg = get_request_msg_without_checksum(request)
    checksum = generate_hmac_sha256_checksum(msg, settings.PG_PARAMS['salt'] )
    msg+= +"|"+ checksum

    return msg
def get_request_msg_without_checksum(request):

    print('request_merchant_2:',  request.data.get('merchant_id'))
    
    msg =   request.data.get('merchant_id')+"|"
    msg +=  request.data.get('unique_transaction_id')+"|"
    msg +=  request.data.get('na_field_1','NA')+"|"
    msg +=  request.data.get('transaction_amount','0')+"|"
    msg +=  request.data.get('na_field_2','NA')+"|"
    msg +=  request.data.get('na_field_3','NA')+"|"
    msg +=  request.data.get('na_field_4','NA')+"|"
    msg +=  request.data.get('currency_type','INR')+"|"
    msg +=  request.data.get('na_field_5','NA')+"|"
    msg +=  request.data.get('type_field_1','NA')+"|"
    msg +=  request.data.get('security_id','NA') +"|"
    msg +=  request.data.get('na_field_6','NA')+"|"
    msg +=  request.data.get('na_field_7','NA')+"|"
    msg +=  request.data.get('na_field_8','NA')+"|"
    msg +=  request.data.get('type_field_2','NA')+"|"
    msg +=  request.data.get('additional_field_1','NA')+"|"
    msg +=  request.data.get('additional_field_2','NA')+"|"
    msg +=  request.data.get('additional_field_3','NA')+"|"
    msg +=  request.data.get('additional_field_4','NA')+"|"
    msg +=  request.data.get('additional_field_5','NA')+"|"
    msg +=  request.data.get('additional_field_6','NA')+"|"
    msg +=  request.data.get('additional_field_7','NA')+"|"
    msg +=  request.data.get('return_url',settings.PG_PARAMS['return_url'])
    return msg

def get_payment_data_request(request):
    print('Merchant:', settings.PG_PARAMS['merchant_code'])
    request.data['merchant_id'] = settings.PG_PARAMS['merchant_code']
    request.data['unique_transaction_id'] = 'LAB-NOC-' + str(random.randint(100000,999999))
    request.data['na_field_1'] = 'NA'
    request.data['transaction_amount'] =  request.data['calculated_fee']
    request.data['na_field_2'] = 'NA'
    request.data['na_field_3'] = 'NA'
    request.data['na_field_4'] = 'NA'
    request.data['currency_type'] = 'INR'
    request.data['na_field_5'] = 'NA'
    request.data['type_field_1'] = 'NA'
    request.data['security_id'] = 'NA'
    request.data['na_field_6'] = 'NA'
    request.data['na_field_7'] = 'NA'
    request.data['type_field_2'] = 'NA'
    request.data['additional_field_1'] = 'NA'
    request.data['additional_field_2'] = 'NA'
    request.data['additional_field_3'] = 'NA'
    request.data['additional_field_4'] = 'NA'
    request.data['additional_field_5'] = 'NA'
    request.data['additional_field_6'] = 'NA'
    request.data['additional_field_7'] = 'NA'
    request.data['return_url'] = settings.PG_PARAMS['return_url']

   
    msg = get_request_msg_without_checksum(request)
    request.data['checksum'] =  generate_hmac_sha256_checksum(msg, settings.PG_PARAMS['salt'] )
    return request

# class PaymentDetailList(generics.ListCreateAPIView):


#     queryset = comm_models.PaymentDetails.objects.all().order_by('-id')
#     serializer_class = comm_serializers.PaymentDetailsSerializers
#     # authentication_classes = (OAuth2Authentication,)
#     # permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         print("Inside candidate application")
       
#         request.data._mutable=True
#         request_data = get_payment_data_request(request=request)

#         request_data.data['user'] = self.request.user.id
#         print(self.request.user.id)
#         request_data.data['created_by'] = self.request.user.id
#         return self.create(self, request_data, *args, **kwargs)
    
#     @transaction.atomic()
#     def perform_create(self, serializer):
#         candidate_application = serializer.save()
#         # self.request.data._mutable=True 
#         # data = self.request.data
       
       
     
#     def create(self, request, *args, **kwargs):
       
#          # Create a serializer for the first model
#         serializer = self.get_serializer(data=self.request.data)
#         print("Error is here in create line")
#         # Validate the first model data
#         serializer.is_valid(raise_exception=True)
#         print("Code has not reched here")
#         # Perform the creation of both models
#         self.perform_create(serializer)
    
#         # Return a response indicating success
#         # headers = self.get_success_headers(serializer.data)
#         # return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         msg= get_request_msg_with_checksum(request=request)
#         return response.Response({'msg':msg}, status=status.HTTP_201_CREATED)
    
#     def get_queryset(self):
#         queryset = comm_models.PaymentDetails.objects.all().order_by('-id')
        
#         # user_info = introspection_sso_user.IntrospectionSSOUser.get(self, self.request)
#         # print("user_info:", user_info)

#         user_id = self.request.user.id
    
#         notification_id= self.request.query_params.get('notification')
#         if user_id:
#             queryset = queryset.filter(created_by=user_id)

#         if notification_id:
#             queryset = queryset.filter(employment_notification = notification_id)
#         return queryset
    

# class PaymentResponseHandler(generics.CreateAPIView):
#     queryset = comm_models.PaymentDetails.objects.all().order_by('-id')
#     serializer_class = comm_serializers.PaymentDetailsSerializers

#     def post(self, request, *args, **kwargs):
#         msg = request.data.get('msg')
#         return response.Response({'msg':msg}, status=status.HTTP_201_CREATED)
     




# class FakePaymentGateWayRequest(generics.CreateAPIView):
#     queryset = comm_models.PaymentDetails.objects.all().order_by('-id')
#     serializer_class = comm_serializers.PaymentDetailsSerializers

#     def post(self, request, *args, **kwargs):
#         request.data._mutable=True
#         request_data = get_payment_data_request(request=request)
#         msg = get_request_msg_with_checksum(request=request_data)
#         payment_url = settings.PG_PARAMS['return_url']

#         html = f"""
#         <html>
#             <body onload="document.forms['billdeskForm'].submit();">
#                 <form id="billdeskForm" action="{payment_url}" method="POST">
#                     <input type="hidden" name="msg" value="{msg}">
                   
#                 </form>
#             </body>
#         </html>
#         """
#         return HttpResponse(html)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# import requests
# import uuid
# import time
# from datetime import datetime, timezone, timedelta
# import hashlib
# from django.utils.dateparse import parse_datetime


# def get_decoded_response(text):
#         # Example JWT token (replace with your token)
       
#         # Your secret key used for signing the token
#         secret_key = settings.PG_PARAMS['salt']

#         try:
#             # Decode and verify the token
#             decoded_payload = jwt.decode(text, secret_key, algorithms=["HS256"])

#             return decoded_payload

#         except jwt.ExpiredSignatureError:
#             return {"Error: The token has expired."}
#         except jwt.InvalidTokenError:
#             return {"Error: Invalid token."}
    
    
# class CreateOrderView(APIView):

#     def create_billdesk_transaction(self, payload, user):
#         try:
#             transaction = comm_models.BillDeskTransaction.objects.create(
#                 mercid=payload.get("mercid"),
#                 orderid=payload.get("orderid"),
#                 amount=payload.get("amount"),
#                 currency=payload.get("currency"),
#                 order_date=parse_datetime(payload.get("order_date")),
#                 ru=payload.get("ru"),
#                 itemcode=payload.get("itemcode"),
                
#                 additional_info1=payload.get("additional_info", {}).get("additional_info1"),
#                 additional_info2=payload.get("additional_info", {}).get("additional_info2"),
                
#                 device_ip=payload.get("device", {}).get("ip"),
#                 device_user_agent=payload.get("device", {}).get("user_agent"),

#                 created_by=user,
#                 updated_by=user
#             )
#             return transaction
#         except Exception as e:
#             print(f"Error creating BillDeskTransaction: {e}")
#             return None
        
#     def update_billdesk_transaction(self, model, data):
#         try:
#             model.bdorderid=data.get('bdorderid')
#             model.itemcode=data.get('itemcode')
#             model.next_step=data.get('next_step')
#             model.objectid=data.get('objectid')
#             model.status=data.get('status')
#             model.createdon=parse_datetime(data.get('createdon'))
#             model.authorization_token=data.get('links',[{},{}])[1].get('headers',{}).get('authorization')
#             model.additional_info1=data.get("additional_info", {}).get("additional_info1"),
#             model.additional_info2=data.get("additional_info", {}).get("additional_info2"),

#             model.save()
            
#             return model
#         except Exception as e:
#             print(f"Error creating BillDeskTransaction: {e}")
#             return None

   
#     def get_browser_fingerprint(self, request):
#         user_agent = request.META.get('HTTP_USER_AGENT', '')
#         ip_address = request.META.get('REMOTE_ADDR', '')
#         accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
#         auth_token = get_auth_token(request)
#         print('auth_token:', auth_token)
#         fingerprint_source = f"{user_agent}|{ip_address}|{accept_language}|{auth_token}"
#         fingerprint_hash = hashlib.sha256(fingerprint_source.encode()).hexdigest()
#         return fingerprint_hash
#     def get_header(self,client_id):
#         header = {
#         "alg": "HS256",
#         "clientid": client_id
#         }
#         return header
    
#     def get_payload(self, request):
#         billdesk_url = settings.PG_PARAMS['payment_request_url']  # Sandbox URL
#          # Replace with your Merchant ID
#         secret_key = settings.PG_PARAMS['salt']  # Replace with your secret key
        
#         # Data from frontend
#         order_id = generate_application_no(self,'ord')
#         return_url =settings.PG_PARAMS['return_url'] # Your callback URL
#         client_id = settings.PG_PARAMS['client_id']
#         fingerprintid = self.get_browser_fingerprint(request)

#         # Define your timezone offset (+05:30)
#         offset = timezone(timedelta(hours=5, minutes=30))

#         # Get the current time in the specified timezone
#         current_time = datetime.now(offset)

#         # Format the time in ISO 8601 without microseconds
#         formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S%z')

#         # Insert colon in timezone offset (+0530 → +05:30)
#         formatted_time = formatted_time[:-2] + ":" + formatted_time[-2:]

          
#     # Payload
#         payload = {
#                     "mercid": settings.PG_PARAMS['merchant_code'],
#                     "orderid": order_id,
#                     "amount": request.data.get("amount"),
#                     "ru": return_url,
#                     "currency": "356",
#                     "order_date": formatted_time,
#                     "additional_info":{
#                         "additional_info1":"NA", 
#                         "additional_info2":"NA"
#                     },
#                     "itemcode":"DIRECT", 
#                     "device":{
#                         "init_channel":"internet", 
#                         "ip":self.get_browser_ip(request),
#                         "user_agent":request.META.get('HTTP_USER_AGENT', ''),
#                         "accept_header":"text/html",
#                         "fingerprintid":fingerprintid, 
#                         "browser_tz":"-330",
#                         "browser_color_depth":"32", 
#                         "browser_java_enabled":"false", 
#                         "browser_screen_height":"601", 
#                         "browser_screen_width":"657", 
#                         "browser_language":"en-US", 
#                         "browser_javascript_enabled":"true"
#                     }
#                  }
#         return payload
   
    
#     def get_browser_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         ip='0.0.0.0'
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]  # First address in the list
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
    
         
#     def post(self, request, *args, **kwargs):
#         # BillDesk configuration
#         billdesk_url = settings.PG_PARAMS['payment_request_url']  # Sandbox URL
#         mercid = settings.PG_PARAMS['merchant_code']  # Replace with your Merchant ID
#         secret_key = settings.PG_PARAMS['salt']  # Replace with your secret key
        
#         # Data from frontend
#         order_id = generate_application_no(self,'ord')
#         amount = request.data.get("amount")
#         return_url =settings.PG_PARAMS['return_url'] # Your callback URL
#         client_id = settings.PG_PARAMS['client_id']

#         headers=self.get_header(client_id)
#         payloads=self.get_payload(request)
        
#         print('headers:', headers)
#         print('payloads:', payloads)

#         # Generate JWS
#         jws = generate_jws_v2(headers,payloads, secret_key)

#         print('jws:', jws)

#         merchant_ids={
#             "mercid":mercid,
#             "clientid":client_id
#         }

#         # Send request to BillDesk
#         headers = {
#             "Content-Type": "application/jose",
#             "Accept":"application/jose",
#             "BD-Traceid": uuid.uuid4().hex[:35],
#             "BD-Timestamp": str(int(time.time() * 1000))
#         }
        
     

#         try:
#             # Send the POST request
#             order=self.create_billdesk_transaction(payloads, self.request.user )
#             print('Order:', order)
           
#             response = requests.post(billdesk_url, data=jws, headers=headers)

#             # Ensure the request was successful
#             response.raise_for_status()

#             # Attempt to parse the response as JSON
#             response_data = response.json()
#             print("Response JSON:", response_data)

#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred: {http_err}")
#             print("Response is not valid JSON:", response.text)
#         except ValueError as json_err:
#             print("Response is not valid JSON:", response.text)
#         except Exception as err:
#             print(f"An error occurred: {err}")

#             print('response:', response)
#             print('response.status_code:', response.status_code)

#         # Handle BillDesk response
#         if response.status_code == 200:
#             # response_data = response.json()
#             decoded_response = get_decoded_response(response.text)

#             order = self.update_billdesk_transaction(order,decoded_response)

           

#             return Response({
#                 "decoded_response": decoded_response,
                
#             })
#         else:
#             return Response(
#                 {
#                     "res_jws": response.text,
#                     "headers_to_pg":headers,
#                     "merchant_ids":merchant_ids,
#                     'jws':jws,
#                 }, status=response.status_code)
    
    
# from rest_framework.views import APIView
# from django.http import HttpResponseRedirect
# import jwt

# class BillDeskCallbackView(APIView):
#     def post(self, request, *args, **kwargs):
#         # Retrieve transaction response
#         # transaction_response = request.data.get("transaction_response")
       
#         if request.data.get('status','')==200:
#            transaction_response = request.data.get("transaction_response",'')
#            transaction_response=get_decoded_response(transaction_response)
        
#         else:
#            transaction_response = get_decoded_response(request.data.get('encrypted_response'))
          
           

#         # Parse and validate the response
#         # (Assuming decryption and checksum validation logic here)
#         secret_key = settings.PG_PARAMS['salt']
#         try:
#             decoded_response = jwt.decode(transaction_response, secret_key, algorithms=["HS256"])
#             # Process decoded response
#             frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_success']+"?res=" + transaction_response
#             return HttpResponseRedirect(frontend_url)
#         except jwt.ExpiredSignatureError:
#             frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_fail']+"?res=" + transaction_response
#             return HttpResponseRedirect(frontend_url)
#         except jwt.InvalidTokenError:
#             frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_fail']+"?res=" + transaction_response
#             return HttpResponseRedirect(frontend_url)
        
#         # Determine the status
#         status = "success"  # Replace with parsed transaction status
#         # frontend_url = f"https://your-frontend.com/payment-{status}"
#         frontend_url = settings.PG_PARAMS['redirect_to_front_end_for_application_fee_paymet_status_page']
        

#         # Redirect to the frontend
       

