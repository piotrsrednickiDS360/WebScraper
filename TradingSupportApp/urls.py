from django.conf import settings
from django.urls import path
from django.conf.urls import *
from . import views

urlpatterns = [
    path('login', views.homepage, name='login'),
    path('mainpage', views.mainpage, name='mainpage'),
    path('registrationpage', views.registrationpage, name='registrationpage'),
    path('filtercompanies', views.filtercompanies, name='filtercompanies'),
    path('unfiltercompanies', views.unfiltercompanies, name='unfiltercompanies'),
    path('scrap', views.scrap_view, name='scrap'),
]