"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from master import views as mst_view

urlpatterns = [
    path('master/district', mst_view.DistrictList.as_view()),
    path('master/district/<int:pk>', mst_view.DistrictList.as_view()),

    path('master/establishment/category', mst_view.EstablishmentCategoryList.as_view()),
    path('master/establishment/category/<int:pk>', mst_view.EstablishmentCategoryDetails.as_view()),

    path('master/office', mst_view.OfficeDetailsList.as_view()),
    path('master/office/<int:pk>', mst_view.OfficeDetailsDetails.as_view()),

    path('master/office/type', mst_view.OfficeTypeList.as_view()),
    path('master/office/type/<int:pk>', mst_view.OfficeTypeDetails.as_view()),

    
]
