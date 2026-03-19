"""AI_POWERED_MEDICAL_PREDICTION URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    path("", views.loginn, name='login'),
    path('admin/', admin.site.urls),
    path("loginn_post", views.loginn_post, name='loginn_post'),
    path("adm_home", views.adm_home, name='adm_home'),
    path("adm_change_password", views.adm_change_password, name='adm_change_password'),
    path('adm_change_password_post',views.adm_change_password_post),
    path("adm_send_notification", views.adm_send_notification, name='send_notification'),
    path("adm_send_notification_post", views.adm_send_notification_post, name='send_notification_post'),
    path("adm_view_hospital", views.adm_view_hospital, name='adm_view_hospital'),
    path("adm_viewfeedback", views.adm_viewfeedback, name='adm_view_feedback'),
    path("adm_viewnotification", views.adm_viewnotification, name='view_notification'),
    path("adm_delete_notification/<id>", views.adm_delete_notification, name='delete_notification'),
    path('logouts',views.logouts),
    path("adm_edit_hospital", views.adm_edit_hospital),
    path("adm_delete_hospital/<id>", views.adm_delete_hospital),


    path("hosp_register", views.hosp_register),
    path("hosp_login", views.hosp_login),
    path("hosp_view_feedback", views.hosp_view_feedback),
    path("hosp_view_notify", views.hosp_view_notify),
    path("hosp_view_profile", views.hosp_view_profile),


    path("alzheimers_predict", views.alzheimers_predict),
    path("bone_fracture_predict", views.bone_fracture_predict),
    path("lung_cancer_predict", views.lung_cancer_predict),
    path("hosp_view_results", views.hosp_view_results),
    path("hospital_send_feedback", views.hospital_send_feedback),

    path('forgotpassword', views.forgotpassword),
    path('forgotpasswordbuttonclick', views.forgotpasswordbuttonclick),
    path('otp', views.otp),
    path('otpbuttonclick', views.otpbuttonclick),
    path('forgotpswdpswed', views.forgotpswdpswed),
    path('forgotpswdpswedbuttonclick', views.forgotpswdpswedbuttonclick),
    path('forgotemail', views.forgotemail),
    path('forgotpass', views.forgotpass),
    path('change_password_hospital',views.change_password_hospital),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)