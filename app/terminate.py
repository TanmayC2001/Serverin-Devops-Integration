# Server - Controller Node termination script (Logout Script)
import boto3
from loaders import BarLoader
import boto3.session

loader = BarLoader()

# terminate instance
aws_session = boto3.Session(profile_name='aws')


def terminate_instance(instance_id):
    loader.start()
    ec2 = aws_session.resource('ec2')
    ec2.instances.filter(InstanceIds=instance_id).stop()
    ec2.instances.filter(InstanceIds=instance_id).terminate()
    loader.stop()
    print("AWS Controller Instance terminated successfully\n")

# 1 EC2 instances status check


def status_check(instance_type):
    
    tags = []
    if instance_type == 'WP':       
        tags.append(instance_type)
    elif instance_type == 'lb':
        tags = ['LB', 'Webserver']    
    else:           
        tags.append(instance_type.capitalize())
    print(tags)
    print("Status Check AWS Controller............\n")
    loader.start()
    conn = aws_session.resource('ec2')
    instances = conn.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': tags}])
    flag_run = 0
    instance_id = []
    for instance in instances:
        if instance.state["Name"] == "running":
            print('Instance exists')
            instance_id.append(instance.id)
            print(instance_id)
            flag_run = 1
    loader.stop()
    # if instances with tag: Contrroller-aws dont exist --->>> initiate one
    if flag_run == 1:
        terminate_instance(instance_id)
    else:
        print("Instance dont exist............\n")


#status_check()

