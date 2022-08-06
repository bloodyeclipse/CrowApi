from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
import uuid

from package.models import Package


class GeoFence(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False, unique=True)
    name = models.CharField(default="", null=False, blank=False, max_length=50)
    is_active = models.BooleanField(default=False)
    geometry = models.PolygonField(srid=4326)

    def __str__(self):
        return self.name


class Device(models.Model):
    uid = uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    code = models.CharField(default="", max_length=10, null=False, blank=False, unique=True)
    mac_address = models.CharField(max_length=25, unique=True, default="", null=False, blank=False)
    package = models.ForeignKey(Package, on_delete=models.DO_NOTHING, )
    description = models.TextField(default="")
    last_location = models.PointField(blank=True, null=True, srid=4326)
    geofence = models.ForeignKey(GeoFence, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.code


class Trip(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    title = models.CharField(default='', max_length=20, blank=False, null=False),
    description = models.TextField()
    pickup = models.PointField(srid=4326)
    destination = models.PointField(srid=4326)
    device = models.ManyToManyField(Device)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class DeviceLocation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False, unique=True)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    location = models.PointField(srid=4326, default=Point(0.0, 0.0))
    in_geofence = models.BooleanField(default=True, )
    speed = models.CharField(default="0", max_length=50)
    sat_count = models.CharField(default=0, max_length=2)
    date_received = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.device.code
