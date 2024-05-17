import boto3
import json

class CreateEC2:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def createNewEC2(cls,data):
        with open("config.json","r") as config:
            ConfData = json.load(config)
        
        aws_access_key_id = ConfData['aws']['accessKey']
        aws_secret_access_key = ConfData['aws']['secretKey']
        region = 'ap-south-1'
        instance_type=None
        ami_id=None
        if data['serverType']=="micro":
            instance_type = 't2.micro'
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
        key_pair_response = ec2.create_key_pair(KeyName=key_name)
        pem_file_path = f"pems/{data['user'].split('@')[0]}/{key_name}.pem"
        with open(pem_file_path, "w") as pem_file:
            pem_file.write(key_pair_response['KeyMaterial'])
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
        lst=[]
        lst.append(instance_id)
        ec2.get_waiter('instance_running').wait(InstanceIds=lst)
        instance_info = ec2.describe_instances(InstanceIds=lst)
        instance = instance_info['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress')
        return (instance_id,public_ip)