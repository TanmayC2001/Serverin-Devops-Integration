# Server - Controller Node initiation script (Login Script)
import boto3
import os
import time
from pathlib import Path
import boto3.session
import sys
#from loaders import BarLoader

#loader = BarLoader()


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

def status_check():
    
    print("Status Check Hadoop Controller............\n")
    #loader.start()
    conn = hadoop_session.resource('ec2')
    instances = conn.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['NameNode']}])
    flag_run = 0
    for instance in instances:
        if instance.state["Name"] == "running":
            print('Instance exists\n')
            flag_run = 1
            return instance.id
    else: 
        print("Instance Dont Exist")    



# fetching public ip


def get_public_ip(instance_id):
    ec2_client = hadoop_session.client("ec2")
    reservations = ec2_client.describe_instances(
        InstanceIds=[instance_id]).get("Reservations")
    print(f"fetching ip of instance :{instance_id}\n\n")
    for reservation in reservations:
        for instance in reservation['Instances']:
            return(instance.get("PublicIpAddress"))


