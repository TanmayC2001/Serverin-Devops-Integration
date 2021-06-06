# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.shortcuts import render 
from app import control_aws_logout, control_hadoop_logout, control_dock_logout

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/dashboard/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'    

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'User created - please <a href="/login">login</a>.'
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid'    
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg" : msg, "success" : success })


def del_cookies(request):
    if request.COOKIES.get('instance') or request.COOKIES.get('hadoop') or request.COOKIES.get('docker'):
        print("Checking Status")
        control_aws_logout.status_check()
        control_hadoop_logout.status_check()
        control_dock_logout.status_check()
        logout(request)
        response = render(request, 'App/home.html')
        response.delete_cookie('instance')
        response.delete_cookie('hadoop')
        response.delete_cookie('docker')
        print("Cookies Deleted")
        return response
    else:
        response = render(request, 'App/home.html')
    logout(request)    
    return response