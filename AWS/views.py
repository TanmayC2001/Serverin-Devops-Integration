from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app.control_aws_login import status_check, get_public_ip
from app import wordpress_status, web_dev_status_check
from app import terminate
from app import instance_status_check
import os
from pathlib import Path
import webbrowser


# Create your views here.



@login_required(login_url="/login/")
def AWS(request):
    segment = 'aws'   
    #return render(request, 'AWS/aws.html', {'segment':segment})    
    #else:
    if request.COOKIES.get('instance') == 'Created':
        print("Cookie Exists")
        return render(request, 'AWS/aws.html', {'segment':segment})
    else:
        response = render(request, 'AWS/aws.html', {'segment':segment})
        response.set_cookie('instance','Created')
        instanceid = status_check()
        ip = get_public_ip(instanceid)
        return response

    if request.method == 'POST':
            service = request.POST.get('button')
            print(service)
    return render(request, 'AWS/aws.html', {'segment':segment})    



def Docs(request):
    segment = 'help aws'
    aws = 1
    return render(request, 'App/docs.html', {'segment':segment, 'aws' : aws})

def Services(request):
        if request.method == 'POST':
            service = request.POST.get('button')
            print(service)
        return render(request, 'AWS/services.html', {'service' : service})

def Instances(request):
    if request.method == 'POST':
            instance_type = request.POST.get('button')
            #Code For Launching Only One Instance
            if request.COOKIES.get('Os') == 'Launched':
                url = "You Cant Launch New Instances "
                return render(request,'AWS/services.html', {'msg':url, 'instance_type':instance_type})
            #If No Instance Is Launched Then Only Will Be Launched
            print(instance_type)
            instance_id = status_check()
            ip = get_public_ip(instance_id)
            print(ip)
            url = run_role(ip, instance_type)
            resp = render(request,'AWS/services.html', {'url':url, 'instance_type':instance_type})
            resp.set_cookie('Os','Launched')
    return resp

# https://13.233.207.181:4200/  Public IP       


def run_role(public_ip_v4,instance_type):
    role_path = f"/home/ec2-user/AWS/aws/{instance_type}.yml"
    pass_file = "/home/ec2-user/AWS/aws/pass.txt"
    key_name = Path("C:/Users/chaud/Downloads/serverin-aws.pem").resolve()
    # print(p)
    # key_name = "aws-serverin"
    cmd = f'ssh -i {key_name} ec2-user@{ public_ip_v4 } -o StrictHostKeyChecking=no sudo ansible-playbook {role_path} --vault-password-file { pass_file }'
    os.system(cmd)
    instance_id = instance_status_check.status_check(instance_type)
    ip = instance_status_check.get_public_ip(instance_id)
    # url = []
    # for i in ip:
    #     url = 
    if instance_type == 'rhel':
        url = f'http://{ip}:9090/system/terminal'
    elif instance_type == 'ubuntu' and 'amazon':    
        url = f'https://{ip}:4200'
    print(url)

    # webbrowser.register('chrome',
    #                 None,
    #                 webbrowser.BackgroundBrowser("C://Program File//Google//Chrome//Application//chrome.exe"))
    # webbrowser.get('chrome').open(url)    
    return url

def Web_dev(request):
    if request.COOKIES.get('Web_Dev') == 'Launched':
        url = "You Cant Launch New Web Development Environment"
        return render(request,'AWS/services.html', {'web_dev_msg':url})
    instance_id = status_check()
    ip = get_public_ip(instance_id)
    url = web_dev_url(ip)
    resp = render(request, 'AWS/services.html', { 'web_dev_ip':url })
    resp.set_cookie('Web_Dev', 'Launched')
    return resp


def Wordpress(request):
    if request.COOKIES.get('Wordpress') == 'Launched':
        url = "You Cant Launch New Wordpress Site"
        return render(request,'AWS/services.html', {'dns_msg':url})
    instanceid = status_check()
    ip = get_public_ip(instanceid)
    url =  wordpress(ip)
    resp = render(request, 'AWS/services.html', { 'dns':url })
    resp.set_cookie('Wordpress', 'Launched')
    return resp

def wordpress(ip):
    role_path = "/home/ec2-user/AWS/aws/wordpress.yml"
    pass_file = "/home/ec2-user/AWS/aws/pass.txt"
    key_name = Path("C:/Users/chaud/Downloads/serverin-aws.pem").resolve()
    # print(p)
    # key_name = "aws-serverin"
    cmd = f'ssh -i {key_name} ec2-user@{ ip } -o StrictHostKeyChecking=no sudo ansible-playbook {role_path} --vault-password-file { pass_file }'
    os.system(cmd)

    # webbrowser.register('chrome',
    #                 None,
    #                 webbrowser.BackgroundBrowser("C://Program File//Google//Chrome//Application//chrome.exe"))
    # webbrowser.get('chrome').open(url)    
    instance_id = wordpress_status.status_check()
    PublicDnsName = wordpress_status.get_public_dns(instance_id)
    url = f'http://{PublicDnsName}/blog'
    return url
    

def web_dev_url(ip):
    print(ip)
    role_path = "/home/ec2-user/AWS/aws/web.yml"
    pass_file = "/home/ec2-user/AWS/aws/pass.txt"
    key_name = Path("C:/Users/chaud/Downloads/serverin-aws.pem").resolve()
    # print(p)
    # key_name = "aws-serverin"
    cmd = f'ssh -i {key_name} ec2-user@{ ip } -o StrictHostKeyChecking=no sudo ansible-playbook {role_path} --vault-password-file { pass_file }'
    os.system(cmd)
    
    instance_id = web_dev_status_check.status_check()
    ip_lb = web_dev_status_check.get_public_ip(instance_id)
    # webbrowser.register('chrome',
    #                 None,
    #                 webbrowser.BackgroundBrowser("C://Program File//Google//Chrome//Application//chrome.exe"))
    # webbrowser.get('chrome').open(url)    
    url = f'http://{ip_lb}:8080'
    return url
    

def Terminate_instance(request):
    if request.method == "POST":
        terminate_type = request.POST.get('Terminate_Button')
        print(terminate_type)
        terminate.status_check(terminate_type)
        msg = "You Have Terminated The Instance Successfully"
        resp = render(request, 'App/index.html', {'msg': msg})
        if terminate_type =='WP':
            resp.delete_cookie('Wordpress')    
        if terminate_type == 'rhel' or 'ubuntu' or 'amazon':
            resp.delete_cookie('Os')
        if terminate_type == 'lb':
            resp.delete_cookie('Web_Dev')    
    return resp
