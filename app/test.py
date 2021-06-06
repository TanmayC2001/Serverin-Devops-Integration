# Retrieviung instance
import boto3
ec2client = boto3.client('ec2')
response = ec2client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'Controller',
            ]
        },
    ],
)
# for reservation in response["Reservations"]:
#     for instance in reservation["Instances"]:
#         # This sample print will output entire Dictionary object
#         # print(instance)
#         # This will print will output the value of the Dictionary key 'InstanceId'
#         print(instance["InstanceId"])


conn = boto3.resource('ec2')
instances = conn.instances.filter()
for instance in instances:
    if instance.state["Name"] == "running":
        print(instance.id, instance.instance_type)
