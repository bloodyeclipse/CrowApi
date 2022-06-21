from django.db import models
from user.models import User
import uuid


class Fleet(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    name = models.CharField(default="", blank=False, null=False, max_length=26)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = "Fleet"
        verbose_name_plural = "Fleets"


class Vehicle(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=20, null=False, auto_created=False, blank=False)
    reg_num = models.CharField(max_length=10, null=False, blank=False, )
    year = models.IntegerField(default=1, auto_created=False)
    millage = models.IntegerField(default=0, max_length=10, auto_created=False, )
    next_service_date = models.DateField(null=True, blank=True)
    next_service_millage = models.IntegerField(null=True, blank=True)
    last_service_date = models.DateField(null=True, blank=True)
    last_service_millage = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_created=True, auto_now=True)
    fleet = models.ForeignKey(Fleet, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"


class VehicleImages(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="vehicles/", default="vroom.png", )
    date_added = models.DateTimeField(auto_created=True, )

    class Meta:
        verbose_name = "Vehicle Image"
        verbose_name_plural = "Vehicle Images"
