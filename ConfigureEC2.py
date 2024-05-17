import boto3
from mongoConnection import MongoCollection
import subprocess
class EC2Configurations:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def getInstanceID(cls,user,instanceName):
        connection=MongoCollection()
        collection=connection.getCollection("VPSDetails")
        instanceId=collection.find_one({'user':user,'vpsName':instanceName})['instanceId']
        return instanceId
    def updateDocument(cls,user,instanceName,update,publicIp):
        connection=MongoCollection()
        collection=connection.getCollection("VPSDetails")
        update = {"$set": {"status":update,"publicIP":publicIp}}
        filter = {'user':user,'vpsName':instanceName}
        collection.update_one(filter, update)
    def deleteDocument(cls,user,instanceName):
        connection=MongoCollection()
        collection=connection.getCollection("VPSDetails")
        collection.delete_one({'user':user,'vpsName':instanceName})

    def startInstance(cls,user,instanceName):
        ec2=boto3.client('ec2')
        a=cls.getInstanceID(user,instanceName)
        lst=[]
        lst.append(a)
        response = ec2.start_instances(InstanceIds=lst)
        ec2.get_waiter('instance_running').wait(InstanceIds=lst)
        instance_info = ec2.describe_instances(InstanceIds=lst)
        instance = instance_info['Reservations'][0]['Instances'][0]
        public_ip = instance.get('PublicIpAddress')
        cls.updateDocument(user,instanceName,"Running",public_ip)
        return "Starting"
    def stopInstance(cls,user,instanceName):
        ec2=boto3.client('ec2')
        a=cls.getInstanceID(user,instanceName)
        lst=[]
        lst.append(a)
        response = ec2.stop_instances(InstanceIds=lst)
        cls.updateDocument(user,instanceName,"Stopped",None)
        return "Stopped"
    def deleteInstance(cls,user,instanceName):
        ec2=boto3.client('ec2')
        a=cls.getInstanceID(user,instanceName)
        lst=[]
        lst.append(a)
        print("deleting")
        response = ec2.terminate_instances(InstanceIds=lst)
        cls.deleteDocument(user,instanceName)
        ec2.delete_key_pair(KeyName=f"{instanceName}-key-pair")
        print("deleted")
        subprocess.run(["rm","-rf",f"pems/{user.split('@')[0]}/{instanceName}-key-pair.pem"])
        return "Terminated"