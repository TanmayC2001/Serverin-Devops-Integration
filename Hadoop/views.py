from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from pathlib import Path
from app.control_hadoop_login import status_check, get_public_ip
from app import hadoop_status 
from django.core.files.storage import FileSystemStorage
# Create your views here.

@login_required(login_url="/login/")
def Hadoop(request):
    segment = 'hadoop'
    if request.COOKIES.get('hadoop') == 'Created':
        print("Cookie Exists")
        instanceid = status_check()
        ip = get_public_ip(instanceid)
        print("Controller Node IP : - ",ip)
        url =  run_role(ip)
        return render(request, 'Hadoop/hadoop.html', {'segment':segment, 'url':url})
    else:
        response = render(request, 'Hadoop/hadoop.html', {'segment':segment})
        instanceid = status_check()
        ip = get_public_ip(instanceid)
        print("Controller Node IP : - ",ip)
        url =  run_role(ip)             
        resp = render(request, 'Hadoop/hadoop.html', {'segment':segment, 'url':url})
        resp.set_cookie('hadoop','Created')
        return resp
    return render(request, 'Hadoop/hadoop.html', {'segment':segment})

def Docs(request):
    segment = 'help hadoop'
    hadoop = 1
    return render(request, 'App/docs.html', {'segment':segment, 'hadoop':hadoop})


def run_role(public_ip_v4,instance_type='hadoop'):
    role_path = f"/home/ec2-user/Hadoop/hadoop/{instance_type}.yml"
    pass_file = "/home/ec2-user/Hadoop/hadoop/pass.txt"
    key_name = Path("C:/Users/chaud/Downloads/serverin-hadoop.pem").resolve()
    # print(p)
    # key_name = "aws-serverin"
    
    cmd = f'ssh -i {key_name} ec2-user@{ public_ip_v4 } -o StrictHostKeyChecking=no sudo ansible-playbook {role_path} --vault-password-file { pass_file }'
    os.system(cmd)
    instance_id = hadoop_status.status_check()
    ip = hadoop_status.get_public_ip(instance_id)
    print("IP Of Instance : - ",ip)
    url = f'http://{ip}:50070'
    
    print(url)
    return url

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'Hadoop/file.html', {
            'uploaded_file_url': uploaded_file_url
        })
    # key_name = Path("C:/Users/chaud/Downloads/hadoop-key.pem").resolve()
    # instance_id = hadoop_status.status_check()
    # ip = hadoop_status.get_public_ip(instance_id)
    # cmd = f'ssh -i {key_name} ec2-user@{ ip } -o StrictHostKeyChecking=no sudo hadoop fs -put '
    # os.system(cmd)  