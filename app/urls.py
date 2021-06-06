# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.home, name='home'),
    path('dashboard/', views.dash, name='dash'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.AboutUs, name='about'),
    path('contact/', views.ContactUs, name='contact'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'), #Used for rendering other static files

]
