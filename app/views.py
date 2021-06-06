# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth.models import User
from authentication.forms import SignUpForm,UserChange
from . import control_aws_login


def home(request):
    segment = 'home'
    # if request.method == "POST":
    #     val = request.POST.get('Val')

    return render(request, 'App/home.html', { 'segment':segment })


@login_required(login_url="/login/")
def dash(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'App/index.html' )
    return HttpResponse(html_template.render(context, request))    
    

#@login_required(login_url="/login/")
#def pages(request):
#    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
#    try:
        
#        load_template      = request.path.split('/')[-1]
#        context['segment'] = load_template
        
#        html_template = loader.get_template( load_template )
#        return HttpResponse(html_template.render(context, request))
        
#    except template.TemplateDoesNotExist:

#        html_template = loader.get_template( 'page-404.html' )
#        return HttpResponse(html_template.render(context, request))

#    except:
    
#        html_template = loader.get_template( 'page-500.html' )
#        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def profile(request):
    segment = 'profile'
    msg=""
    if request.method == 'POST':
        fm = UserChange(request.POST,instance=request.user)
        if fm.is_valid():
            msg = "Your Form Has Been Saved Successfully"
            fm.save()
            return render(request, 'App/page-user.html', {'segment':segment, 'form':fm , 'msg':msg})
    else:
        fm = UserChange(instance=request.user)
        msg = ""
        return render(request, 'App/page-user.html', {'segment':segment, 'form':fm , 'msg':msg})
    
    return render(request, 'App/page-user.html', {'segment':segment, 'form':fm , 'msg':msg})     

def AboutUs(request):
    segment = 'info'
    return render(request, 'App/about.html', {'segment':segment})

def ContactUs(request):
    segment = 'contact'
    return render(request, 'App/contact.html', {'segment':segment})

