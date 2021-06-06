# Server - Controller Node termination script (Logout Script)
import boto3
import boto3.session
from loaders import BarLoader

loader = BarLoader()

# terminate instance
hadoop_session = boto3.Session(profile_name='hadoop')


def terminate_instance(instance_id):
    loader.start()
    ec2 = hadoop_session.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_id).stop()
    ec2.instances.filter(InstanceIds=instance_id).terminate()
    loader.stop()
    print("Hadoop Controller Instance terminated successfully\n")

# 1 EC2 instances status check


def status_check():
    print("Status Check Hadoop Controller............\n")
    loader.start()
    conn = hadoop_session.resource('ec2')
    instances = conn.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Controller-hadoop', 'NameNode', 'DataNode']}])
    flag_run = 0
    for instance in instances:
        if instance.state["Name"] == "running":
            print('Instance exists')
            instance_id = []
            instance_id.append(str(instance.id))
            print(instance_id)
            flag_run = 1
    loader.stop()
    print("These Are Instance ID's")
    print(instance_id)
    # if instances with tag: Contrroller dont exist --->>> initiate one
    if flag_run == 1:
        terminate_instance(instance_id)
    else:
        print("Instance dont exist............\n")


# status_check()
