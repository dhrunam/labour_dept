"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
from rest_framework.settings import api_settings
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e@3qi5*fd6ck+vf^4%lqru0m(@xx8$!x-==$-j_95j*tvw9*_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'https://labour.diseso.com'

]
CORS_ORIGIN_ALLOW_ALL = False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'durin',
    'account',
    'master',
    'configuration',
    'operation',
    'common',
    'drf_api_logger',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'labour_dept_stage_db',
        'USER': 'postgres',
        'PASSWORD': 'Darkhorse@7428',
        'HOST': '93.127.199.87', 
        'PORT': '5432'
    },

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'labour_dept_db',
    #     'USER': 'postgres',
    #     'PASSWORD': 'postgres',
    #     'HOST': 'localhost', 
    #     'PORT': '5432'
    #  }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)  '   
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        # 'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('durin.auth.TokenAuthentication',),
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    "DEFAULT_THROTTLE_CLASSES": ["durin.throttling.UserClientRateThrottle"],
    "DEFAULT_THROTTLE_RATES":{'user_per_client': '20/min'},
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10,
}

REST_DURIN = {
        "DEFAULT_TOKEN_TTL": timedelta(days=1),
        "TOKEN_CHARACTER_LENGTH": 64,
        "USER_SERIALIZER": 'account.serializers.UserSerializer',
        "AUTH_HEADER_PREFIX": "Token",
        "EXPIRY_DATETIME_FORMAT": api_settings.DATETIME_FORMAT,
        "TOKEN_CACHE_TIMEOUT": 60,
        "REFRESH_TOKEN_ON_LOGIN": False,
        "AUTHTOKEN_SELECT_RELATED_LIST": ["user"],
        "API_ACCESS_CLIENT_NAME": ['web','mobile','cli'],
        "API_ACCESS_EXCLUDE_FROM_SESSIONS": False,
        "API_ACCESS_RESPONSE_INCLUDE_TOKEN": False,
}


USER_ROLES = {
    "superadmin":"superadmin",
    "general_user":"general_user",
    "level1_dept_admin": "level1_dept_admin",
    "level2_dept_admin": "level2_dept_admin",
    "level3_dept_admin": "level3_dept_admin",
}


INTIMATION_TYPE = {
    "FEE_INTIMATION":'fee_intimation',
    "REPLY_INTIMATION":'reply_intimation',
}

APPLICATION_STATUS={
    # "forwarded":"forwarded",
    "received":"received",
    "rejected":"rejected",
    # "pending" : "pending",
    "approved" : "approved",
    # "completed":"completed",
    'fee_payment_success' : 'fee_payment_success',
    "t1-verification":"T1-Verification",
    "t2-verification":"T2-Verification",

}

# PG_PARAMS={}

# if DEBUG:
#     PG_PARAMS={: "https://www.sbsebr.com/sbsuat/UATInitiateTransaction/GetTransactionStatus" ,
#     }
# else:
#     PG_PARAMS={
#         "merchant_code" : "HCOSb6b7653647703084793cc9",
#         "major_head_code" : "0070",
#         "minor_head_code" : "01.501",
#         "return_url" : "https://eservices.hcs.nic.in/api/rti/payment/response",
#         "redirect_to_front_end_for_application_fee_paymet_status_page" : "https://eservices.hcs.nic.in/dashboard/payment?application=",
#         "redirect_to_front_end_for_intimation_fee_paymet_status_page" : "https://eservices.hcs.nic.in/dashboard/payment?application=",
#         "salt" : "05f4d50ce3450363b07a0772f9fd82f403f44cb3feee37700ebac9b8fc33d51f",
#         "payment_request_url" : "https://www.sbsebr.com/sbslive/InitiateTransaction/PaymentRequestGOS" ,
#         "payment_status_url" : "https://www.sbsebr.com/sbslive/InitiateTransaction/GetTransactionStatus" ,
#     }

PAYMENT_FOR = {
    "rti_application" : "RTI Application",
    "rti_intimation" : "RTI Intimation",
}

PG_PAYMENT_STATUS = {
    'initiated': 'Initiated',
    'success' : 'Success',
    'failure': 'Failure',
    'pending' : 'Pending',
}

SMS_TEMPLATE = {
    "received":{"template_id": '1107168810350264462',
                "message": "We have received your RTI Application {application_no} on {app_date}. You can now check you application status by logging in in our website. -High Court of Sikkim"
                },
    "completed":{"template_id":'1107168810246154241',
                "message": "Message: Your RTI Application {application_no} has been completed on {app_date}. -High Court of Sikkim"
                },
    "rejection":{"template_id":'1107168810252194828',
                "message": "Message: Your RTI Application {application_no} has been rejected on {app_date} due to following reason: {reason} -High Court of Sikkim"
                },
    "intimation":{"template_id":'1107168810554316987',
                "message": "Your RTI Application {application_no} has been processed. Please pay the amount of Rs. {fee} by logging in in our website and by clicking 'Pay Additional Fees' for the respective application to proceed further. -High Court of Sikkim"
                },
    "first_appeal":{"template_id":'1107168810274966417',
                "message": "Message: We have received the request for First Appeal for RTI Application {application_no} on {app_date}. -High Court of Sikkim"
                },
    "forwarded":{"template_id":'1107168810279676706',
                "message": "Your RTI Application {application_no} has been forwarded to {forwarded_to} on {app_date}. -High Court of Sikkim"
                },
}

APP_MODULES={

}

PG_PARAMS={}

if DEBUG:
    PG_PARAMS={
        "merchant_code" : "BDSKUATY",
        "client_id":"bdskuaty",
        # "major_head_code" : "0215",
        # "minor_head_code" : "01.103",
        # "return_url" : "https://api.diseso.com/api/application/online_payment/callback",
        "return_url" : "http://localhost:8000/api/application/online_payment/callback",
        "redirect_to_front_end_for_application_fee_paymet_success" : "http://localhost:4200/dashboard/shops-establishment/payment/success",
        "redirect_to_front_end_for_application_fee_paymet_fail" : "http://localhost:4200/dashboard/shops-establishment/payment/fail",
        "salt" : "G3eAmyVkAzKp8jFq0fqPEqxF4agynvtJ",
        "payment_request_url" : "https://uat.billdesk.com/pgidsk/PGIMerchantPayment" ,
        "payment_status_url" : "https://www.sbsebr.com/sbsuat/UATInitiateTransaction/GetTransactionStatus" ,
    }
   
else:
    PG_PARAMS={
       "merchant_code" : "BDSKUATY",
       "client_id":"bdskuaty",
        # "major_head_code" : "0215",
        # "minor_head_code" : "01.103",
        "return_url" : "https://api.diseso.com/api/application/online_payment/callback",
        "redirect_to_front_end_for_application_fee_paymet_success" : "https://labour.diseso.com/dashboard/shops-establishment/payment/success",
        "redirect_to_front_end_for_application_fee_paymet_fail" : "https://labour.diseso.com/dashboard/shops-establishment/payment/fail",
        "salt" : "tKU9WjmyRiJTRyR4z5PGDY9VrzMV2MS0",
        "payment_request_url" : "https://uat1.billdesk.com/u2/payments/ve1_2/orders/create" ,
        "payment_status_url" : "https://www.sbsebr.com/sbsuat/UATInitiateTransaction/GetTransactionStatus" ,
    }

#Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply.labour.dept.sikkim@gmail.com'
EMAIL_HOST_PASSWORD = 'Ubuntu@123'

# Logger specific configuration
DRF_API_LOGGER_DATABASE = True
DRF_LOGGER_QUEUE_MAX_SIZE = 50 
DRF_LOGGER_INTERVAL = 10 
DRF_API_LOGGER_SKIP_NAMESPACE = []
DRF_API_LOGGER_SKIP_URL_NAME =[]
DRF_API_LOGGER_EXCLUDE_KEYS = ['password', 'token', 'access', 'refresh']
DRF_API_LOGGER_DEFAULT_DATABASE = 'default'
DRF_API_LOGGER_SLOW_API_ABOVE = 200
DRF_API_LOGGER_METHODS = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']
# DRF_API_LOGGER_STATUS_CODES = ['200', '400', '404', '500']
DRF_API_LOGGER_STATUS_CODES = []
DRF_API_LOGGER_TIMEDELTA = 330 # UTC + 330 Minutes = IST (5:Hours, 30:Minutes ahead from UTC)



