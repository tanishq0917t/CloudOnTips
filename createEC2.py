import boto3


aws_access_key_id = ''
aws_secret_access_key = ''
region = 'ap-south-1'


instance_type = 't2.micro'
ami_id = 'ami-0f58b397bc5c1f2e8'
key_name = '-pair'
security_group_ids = ['launch-wizard-1']
volume_size = 30

ec2 = boto3.client('ec2', region_name=region,
                   aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key)


block_device_mappings = [{
    'DeviceName': '/dev/xvda',
    'Ebs': {
        'VolumeSize': volume_size,
        'VolumeType': 'gp2'
    }
}]


response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    KeyName=key_name,
    SecurityGroupIds=security_group_ids,
    MaxCount=1,
    MinCount=1,
    InstanceInitiatedShutdownBehavior='stop',
    BlockDeviceMappings=block_device_mappings
)


instance_id = response['Instances'][0]['InstanceId']
print("Instance ID:", instance_id)
print("Waiting for instance to be running...")
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])


ec2.stop_instances(InstanceIds=[instance_id])
print("Instance stopped.")