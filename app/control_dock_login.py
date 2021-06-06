# Server - Controller Node initiation script (Login Script)
import boto3
import os
import boto3.session
import time
from pathlib import Path
from loaders import BarLoader
import webbrowser


#########################################
loader = BarLoader()


# Resolving windows path
p = Path("C:/Users/chaud/Downloads/serverin-docker.pem").resolve()
print(p)
# Subnet ID
subnetId = "subnet-54f5e53c"
# Security Group
securityGroup = 'sg-0d04ccf9152eb267b'
# Image Id
imageId = "ami-0e5554737119c59e7"
# Instace type
instanceType = 't2.micro'
# key name
keyName = 'serverin-docker'


docker_session = boto3.Session(profile_name='docker')

# 2 Instance launcher


def create_instance():
    print('creating instance.............\n\n')
    loader.start()
    ec2 = docker_session.resource('ec2')
    instances = ec2.create_instances(
        ImageId=imageId,
        MinCount=1,
        MaxCount=1,
        InstanceType=instanceType,
        KeyName=keyName,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Controller-docker'
                    },
                ]
            },
        ],
        NetworkInterfaces=[
            {
                'DeviceIndex': 0,
                'SubnetId': subnetId,
                'Groups': [
                    securityGroup,
                ],
                'AssociatePublicIpAddress': True
            }],
    )
    instances[0].wait_until_running()
    print("\nWait for ssh to comeup.....\n\nRequired 60 seconds.........\n\n")
    loader.stop()
    loader.start()
    time.sleep(80)
    loader.stop()
    return(instances[0])


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
            print('Instance exists\n')
            flag_run = 1
    loader.stop()
    # if instances with tag: Contrroller dont exist --->>> initiate one
    if flag_run != 1:
        instance_id = create_instance()
        instance_id = instance_id.id
        print(instance_id)
        return(instance_id)
    else:
        # retruning existing id
        return(instance.id)


# instance_id = status_check()

# fetching public ip


def get_public_ip(instance_id):
    ec2_client = docker_session.client("ec2")
    reservations = ec2_client.describe_instances(
        InstanceIds=[instance_id]).get("Reservations")
    print(f"fetching ip of instance :{instance_id}\n\n")
    for reservation in reservations:
        for instance in reservation['Instances']:
            return(instance.get("PublicIpAddress"))


# public_ip_v4 = get_public_ip(instance_id)
# print(f"Fetched IP : {public_ip_v4}\n\n")
##################################################