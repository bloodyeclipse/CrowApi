from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceLocation)
admin.site.register(GeoFence)
admin.site.register(Trip)
