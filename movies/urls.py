"""movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
      path('adminmovies/',views.admin),
       path('getenddate/',views.getenddate),
       path('upmovies/',views.upmovie),
      path('upload/',views.uploads),
      path('movieenter/',views.enter),
      path('updatescreen/',views.updatescreen),
     path('',views.index),
         path('modify/register.html',views.register),
 		        path('checkdata/',views.checkdata),
 		        path('checkgoogle/',views.google),
 		           path('signup/',views.signup),                
	           path('signin/',views.signin),                
        path('profile/',views.profile),
        path('changemobile/',views.changemobile),
        path('deleteotp/',views.deleteotp),
        path('validateotp/',views.validateotp),
    path('sendsms/',views.sendSMS),
 	path('getscreening/',views.getscreening),
 	path('getscreendetails/',views.getscreendetails),
 	path('updatepsw/',views.updatepsw),
 	path('checkseats/',views.checkseats),
 	path('sendseattomob/',views.sendseattomob),
 		path('getmovies/',views.getmovies),
 	path('sendemail/',views.sendemail),
 	       path('LOGOUT/',views.logout)       
]
