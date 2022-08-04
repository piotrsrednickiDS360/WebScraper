from django.conf import settings
from django.urls import path
from django.conf.urls import *
from . import views

urlpatterns = [
    path('homepage', views.homepage, name='homepage'),
    path('mainpage', views.mainpage, name='mainpage'),
    path('registrationpage', views.registrationpage, name='registrationpage'),
]