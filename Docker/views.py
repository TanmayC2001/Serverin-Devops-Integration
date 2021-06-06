from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.control_dock_login import status_check, get_public_ip
from pathlib import Path
import os

# Create your views here.

@login_required(login_url="/login/")
def Docker(request):
    segment = 'docker'
    if request.COOKIES.get('docker') == 'Launched':
        resp = render(request, 'Docker/docker.html', {'segment':segment})
    else:
        response = render(request, 'Hadoop/hadoop.html', {'segment':segment})
        instanceid = status_check()
        ip = get_public_ip(instanceid)
        resp = render(request, 'Docker/docker.html', {'segment':segment})
        resp.set_cookie('docker','Launched')

    return resp        

def Docs(request):
    segment = 'help docker'
    docker = 1
    return render(request, 'App/docs.html', {'segment':segment, 'docker':docker})


def Docker_service(request):
    if request.method == "POST":
        if request.COOKIES.get('ML') == 'Launched':
            msg = 'Beta Masti Nahi'
            resp = render(request,'Docker/services.html', { 'msg':msg })
        else:
            model = request.POST.get('ml')
            instanceid = status_check()
            ip = get_public_ip(instanceid)
            url = run_role(ip)
            resp = render(request,'Docker/services.html', { 'url':url })
            resp.set_cookie("ML", "Launched")
    return resp    




def run_role(public_ip_v4):
    
    key_name = Path("C:/Users/chaud/Downloads/serverin-docker.pem").resolve()
    cmd = f'ssh -i {key_name} ec2-user@{ public_ip_v4 } -o StrictHostKeyChecking=no sudo docker start webapp'
    os.system(cmd)
    url = f'http://{public_ip_v4}'
    print(url)
    return url    

def Terminate_model(request):
    if request.method == "POST":
        instance_id = status_check()
        public_ip_v4 = get_public_ip(instance_id)
        key_name = Path("C:/Users/chaud/Downloads/serverin-docker.pem").resolve()
        cmd = f'ssh -i {key_name} ec2-user@{ public_ip_v4 } -o StrictHostKeyChecking=no sudo docker stop webapp'
        os.system(cmd)
        msg = "Deployment Terminated Successfully..."
        resp = render(request, 'Docker/docker.html', {'msg' : msg})
        resp.delete_cookie('ML')
    return resp 