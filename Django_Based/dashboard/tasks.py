from celery import shared_task
import boto3
import os
import time
from django.conf import settings
from .models import vps_details

@shared_task
def _create_EC2(data):
    time.sleep(10)
    return "Hello"


@shared_task
def create_EC2(data):
    aws_access_key_id=os.getenv('ACCESS_KEY')
    aws_secret_access_key=os.getenv('SECRET_KEY')
    region = 'ap-south-1'
    instance_type=None
    ami_id=None
    
    #Setting up the configurations for EC2 Instance
    
    if data['serverType']=="micro": instance_type = 't2.micro'
    ami_id = data['serverOS']
    key_name = f"{data['serverName']}-key-pair"
    security_group_ids = ['launch-wizard-1']
    volume_size = int(data['serverStorage'])

    ec2 = boto3.client('ec2', region_name=region,aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key)
    block_device_mappings = [{
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': volume_size,
                'VolumeType': 'gp2'
            }
        }]
    

    #Creating PEM file
    key_pair_response = ec2.create_key_pair(KeyName=key_name)
    static_folder = os.path.join(settings.BASE_DIR, 'static')
    pem_file_path = os.path.join(static_folder, f"pems/{data['user']}/{key_name}.pem")
    with open(pem_file_path, "w") as pem_file:
        pem_file.write(key_pair_response['KeyMaterial'])
    
    #Starting the instance (Fresh Start)
    instance_response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids,
        MinCount=1,
        MaxCount=1,
        BlockDeviceMappings=block_device_mappings,
        TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': data['serverName']
                        },
                    ]
                }
            ]
        )
    instance_id = instance_response['Instances'][0]['InstanceId']
    lst=[instance_id]
    ec2.get_waiter('instance_running').wait(InstanceIds=lst)
    instance_info = ec2.describe_instances(InstanceIds=lst)
    instance = instance_info['Reservations'][0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress')
    vps=vps_details.objects.get(name=data['serverName'],user=data['user'])
    vps.status="Running"
    vps.ip_addr=public_ip
    vps.pem_name=key_name
    vps.save()
    return (instance_id,public_ip)