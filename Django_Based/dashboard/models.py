from django.db import models


class vps_details(models.Model):
    name=models.CharField()
    storage=models.IntegerField()
    os=models.CharField()
    type=models.CharField()
    user=models.CharField()
    task_id=models.CharField(default='None')
    status=models.CharField(default='Stopped')
    ip_addr=models.CharField(default='-')
    pem_name=models.CharField(default='-')