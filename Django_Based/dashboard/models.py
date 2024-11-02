from django.db import models


class vps_details(models.Model):
    name=models.CharField()
    storage=models.IntegerField()
    os=models.CharField()
    type=models.CharField()
    user=models.CharField()


