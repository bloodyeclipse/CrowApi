from django.db import models
import uuid
from django.conf.global_settings import AUTH_USER_MODEL


class HazardLevel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    name = models.CharField(max_length=30, unique=True, default="Hazard Name")
    description = models.CharField(max_length=125, default="Hazard Description")
    color = models.CharField(max_length=15, default="#207aab6b")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hazard Level"
        verbose_name_plural = "Hazard Levels"


class PackageType(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    name = models.CharField(max_length=50, default="Name")
    description = models.CharField(max_length=120)
    hazard = models.ForeignKey(HazardLevel, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Package Type"
        verbose_name_plural = "Package Types"


class Package(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    name = models.CharField(default="Package name", max_length=40)
    description = models.CharField(default="Package Description", max_length=120)
    attr = models.JSONField(default=dict, )
    package_type = models.ForeignKey(PackageType, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_created=True, auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"


class PackageImage(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, auto_created=True, null=False, blank=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    description = models.CharField(max_length=35, default="", null=True, blank=True)

    def __str__(self):
        return self.package.name
