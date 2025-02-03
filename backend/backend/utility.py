from datetime import datetime
import time
import requests, random
from django.core.mail import send_mail
from operation import models as op_models



def generate_id_for_file_name(self, prepend):

    two_digit_year = datetime.now().year % 100
    reservation_month =datetime.now().month
    # now = time.time()
    milliseconds = random.randint(100000,999999) ##int(now * 1000)

    return prepend  + f"{reservation_month:02d}" + str(two_digit_year)+str(milliseconds)


def file_upload_handler(self, request):
        file_number = generate_id_for_file_name(self, "id")
        file_name_parts = ""
        if 'id_proof' in request.FILES:
            file_name_parts = request.data['id_proof'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['id_proof'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]
        if 'photograph_applicant' in request.FILES:
            file_name_parts = request.data['photograph_applicant'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['photograph_applicant'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]
        if 'trade_licence' in request.FILES:
            file_name_parts = request.data['trade_licence'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['trade_licence'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]
        
        if 'registration_certificate' in request.FILES:
            file_name_parts = request.data['registration_certificate'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['registration_certificate'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]
      
        
              
        return request

def send_sms(to_mobile_number, template_id, message):

    username = ''
    pin = ''
    signature = ''
    entity_id = ''
    # template_id = sms_template[template_name]['template_id']
    # message = sms_template[template_name]['message']
    #template_id = '1107165390653742984'
    print("message", message)
    try:
        url = ""+username+"&pin="+pin+"&message="+message+"&mnumber="+to_mobile_number+"&signature="+signature+"&dlt_entity_id="+entity_id+"&dlt_template_id="+template_id
        requests.get(url, verify=False)
        print('Message Sent')
        return None
    except Exception as e:
        print(e)

def send_emil_from_app(self, request):
        subject = 'Subject here'
        message = 'Here is the message.'
        from_email = 'your_email@gmail.com'
        recipient_list = ['recipient@example.com']
        send_mail(subject, message, from_email, recipient_list)



def generate_application_no(self,prefix):
        print("Prefixed:", prefix)
        model=op_models.ApplicationNumberSequence
        # prefix='GOS-DL-GTK'
        latest_record = op_models.ApplicationNumberSequence.objects.filter(prefix=prefix).last()

        sl_no = 1
        if latest_record:
            sl_no = latest_record.sequence
            print('Application No:',sl_no)
            if sl_no:
                sl_no = sl_no +1

            latest_record.sequence = sl_no
            latest_record.save()
        else:
            model.objects.create(
                prefix=prefix,
                sequence = sl_no
                )

        return prefix + '-' + f"{sl_no:05d}"

import hmac
import hashlib

def generate_hmac_sha256_checksum(input_string, secret_key):
    # Encode the input string and key as bytes
    input_bytes = input_string.encode('utf-8')
    key_bytes = secret_key.encode('utf-8')
    
    # Create an HMAC object using SHA-256
    hmac_hash = hmac.new(key_bytes, input_bytes, hashlib.sha256)
    
    # Get the hexadecimal representation of the hash
    checksum = hmac_hash.hexdigest()
    return checksum


import hashlib
import base64
import json
import hmac

def generate_jws_v1(header,payload,secret_key):
#     # Header
#     header = {
#         "alg": "HS256",
#         "clientid": client_id
#     }
    
#     # Payload
#     payload = {
#         "mercid": mercid,
#         "orderid": orderid,
#         "amount": amount,
#         "ru": ru,
#         "currency": "356",
#         "order_date": datetime.now(),
#         "additional_info":{
#             "additional_info1":"NA", 
#             "additional_info2":"NA"
#         },
#         "itemcode":"DIRECT", 
#         "device":{
#             "init_channel":"internet", 
#             "ip":"<customer’s ip>",
#             "user_agent":"Mozilla/5.0(WindowsNT10.0;WOW64;rv:51.0)Gecko/20100101 Firefox/51.0",
#             "accept_header":"text/html", "fingerprintid":"61b12c18b5d0cf901be34a23ca64bb19", "browser_tz":"-330",
#             "browser_color_depth":"32", "browser_java_enabled":"false", "browser_screen_height":"601", "browser_screen_width":"657", "browser_language":"en-US", "browser_javascript_enabled":"true"
# }

#     }
    
    # Base64-encode header and payload
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    # Generate the signature
    data_to_sign = f"{header_encoded}.{payload_encoded}"
    signature = hashlib.sha256(f"{data_to_sign}|{secret_key}".encode()).hexdigest()
    
    
    # Return the JWS
    return f"{header_encoded}.{payload_encoded}.{signature}"

def generate_jws_v2(header, payload, secret_key):
    # Base64-encode the header and payload
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().strip('=')
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().strip('=')
    
    # Generate the string to sign
    data_to_sign = f"{header_encoded}.{payload_encoded}"
    
    # Create the signature using HMAC with SHA-256
    signature = hmac.new(
        secret_key.encode(),
        data_to_sign.encode(),
        hashlib.sha256
    ).digest()
    
    # Base64-encode the signature
    signature_encoded = base64.urlsafe_b64encode(signature).decode().strip('=')
    
    # Return the JWS
    return f"{header_encoded}.{payload_encoded}.{signature_encoded}"


def get_auth_token(request):
    auth_header = request.headers.get('Authorization', None)

    if auth_header is None:
        return ''

        # Token is usually in the format "Token <actual_token>"
    if auth_header.startswith("Token "):
            return auth_header.split(" ")[1]
    else:
       return ''
