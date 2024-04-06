from datetime import datetime
import time


def generate_id_for_file_name(self, prepend):

    two_digit_year = datetime.now().year % 100
    reservation_month =datetime.now().month
    now = time.time()
    milliseconds = int(now * 1000)

    return prepend  + f"{reservation_month:02d}" + str(two_digit_year)+str(milliseconds)


def file_upload_handler(self, request):
        file_number = generate_id_for_file_name(self, "applicant_photo")
        if 'photograph_applicant' in request.FILES:
            file_name_parts = request.data['photograph_applicant'].name.split(
                        '.')
            if len(file_name_parts) > 1:
                        request.data['photograph_applicant'].name = file_number + '.'+file_name_parts[len(file_name_parts)-1]

              
        return request

