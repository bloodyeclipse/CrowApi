from django.db import models
import uuid

from package.models import Package


class Device(models.Model):
    uid = uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    code = models.CharField(default="", max_length=10, null=False, blank=False, unique=True)
    mac_address = models.CharField(max_length=25, unique=True, default="", null=False, blank=False)
    package = models.ForeignKey(Package, on_delete=models.DO_NOTHING, )
    description = models.TextField()

    def __str__(self):
        return self.code


class DeviceLocation(models.Models):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False, unique=True)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    latitude = models.CharField(default="", max_length=50, null=False, blank=False)
    longitude = models.CharField(default="", max_length=50, null=False, blank=False)
    speed = models.CharField(default="0", max_length=50)
    sat_count = models.CharField(default=0, max_length=2)
    date_received = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.device.code
