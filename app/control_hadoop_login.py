# Server - Controller Node initiation script (Login Script)
import boto3
import os
import time
from pathlib import Path
from loaders import BarLoader
import boto3.session

loader = BarLoader()


# Resolving windows path
p = Path("c:/Users/chaud/Downloads/serverin-hadoop.pem").resolve()
print(p)
# Subnet ID
subnetId = 'subnet-f119f49a'
# Security Group
securityGroup = 'sg-04d1ee2ac17d0ffd0'
# Image Id
imageId = "ami-0d1fe30d6f009a2ec"
# Instace type
instanceType = 't2.micro'
# key name
keyName = 'serverin-hadoop'


hadoop_session = boto3.Session(profile_name='hadoop')

# 2 Instance launcher


def create_instance():
    print('creating instance.............\n\n')
    loader.start()
    ec2 = hadoop_session.resource('ec2')
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
                        'Value': 'Controller-hadoop'
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
    conn = hadoop_session.resource('ec2')
    instances = conn.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Controller-hadoop']}])
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


#instance_id = status_check()

# fetching public ip


def get_public_ip(instance_id):
    ec2_client = hadoop_session.client("ec2")
    reservations = ec2_client.describe_instances(
        InstanceIds=[instance_id]).get("Reservations")
    print(f"fetching ip of instance :{instance_id}\n\n")
    for reservation in reservations:
        for instance in reservation['Instances']:
            return(instance.get("PublicIpAddress"))


# public_ip_v4 = get_public_ip(instance_id)
# print(f"Fetched IP : {public_ip_v4}\n\n")
