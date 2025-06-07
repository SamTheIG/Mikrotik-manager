from django.db import models
from django.contrib.auth.models import User


class Mikrotik(models.Model):
    Mikid = models.AutoField(primary_key=True)
    Userid = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    MikUsername = models.CharField(max_length=50, null=False)
    MikPassword = models.CharField(max_length=100, null=False)
    MikName = models.CharField(max_length=50, null=False)
    MikIp = models.CharField(max_length=15, null=False)
    MikPort = models.PositiveIntegerField(null=False)
    MikCreatedDate = models.DateTimeField(auto_now_add=True, null=False)


    def __str__(self):
        return self.MikName


class Hotspot(models.Model):
    Hotspot_id = models.ForeignKey("Mikrotik", on_delete=models.CASCADE, null=False)
    uname = models.CharField(max_length=100, null=False)
    upass = models.CharField(max_length=100, null=False)
    speed = models.IntegerField(null=False)
    upload = models.IntegerField(null=False)
    download = models.IntegerField(null=False)
    createdDate = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.uname
