# Server - Controller Node termination script (Logout Script)
import boto3
from loaders import BarLoader
import boto3.session

loader = BarLoader()

# terminate instance
docker_session = boto3.Session(profile_name='docker')


def terminate_instance(instance_id):
    loader.start()
    ec2 = docker_session.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_id).stop()
    ec2.instances.filter(InstanceIds=instance_id).terminate()
    loader.stop()
    print("Instance terminated successfully\n")

# 1 EC2 instances status check


def status_check():
    print("Status Check............\n")
    loader.start()
    conn = docker_session.resource('ec2')
    instances = conn.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Controller-docker']}])
    flag_run = 0
    for instance in instances:
        if instance.state["Name"] == "running":
            print('Instance exists')
            instance_id = []
            instance_id.append(str(instance.id))
            print(instance_id)
            flag_run = 1
    loader.stop()
    # if instances with tag: Contrroller dont exist --->>> initiate one
    if flag_run == 1:
        terminate_instance(instance_id)
    else:
        print("Instance dont exist............\n")


# status_check()
# ssh -i "" ec2-user@{ip} sudo ansible-playbook {playbook} --vault-pass-file pass.txt
