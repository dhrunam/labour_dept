from datetime import datetime
import time
import requests
from django.core.mail import send_mail
from operation import models as op_models



def generate_id_for_file_name(self, prepend):

    two_digit_year = datetime.now().year % 100
    reservation_month =datetime.now().month
    now = time.time()
    milliseconds = int(now * 1000)

    return prepend  + f"{reservation_month:02d}" + str(two_digit_year)+str(milliseconds)


def file_upload_handler(self, request):
        file_number = generate_id_for_file_name(self, "id")
        if 'id_proof' in request.FILES:
            file_name_parts = request.data['id_proof'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['id_proof'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]

              
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
        model=op_models.ApplicationNumberSequence
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

        return prefix + '-' + str(sl_no)   
