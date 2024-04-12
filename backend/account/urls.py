from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account import views as acc_views

urlpatterns = [
     path('otp', acc_views.UserOtpList.as_view()),
    path('otp/forgotpassword', acc_views.OtpForForgetPassword.as_view()),
    path('user/register', acc_views.UserCreate.as_view()),
    path('admin/user/register', acc_views.UserCreateFromAdmin.as_view()),
    path('user/<int:pk>', acc_views.UserRetrieve.as_view()),
    path('user/list', acc_views.UserList.as_view()),
    path('user/update/<int:pk>', acc_views.UserUpdate.as_view()),
    path('admin/user/update/<int:pk>', acc_views.UserUpdateByAdmin.as_view()),
    path('user/profile/update/<int:pk>', acc_views.UserProfileDetails.as_view()),
    path('user/forgotpassword/change',acc_views.UserForgotPasswordChange.as_view()),
    path('group', acc_views.GroupList.as_view()),
    path('group/<int:pk>', acc_views.GroupDetails.as_view()),
     path('auth/',include('durin.urls')),
]
