from django.contrib import admin
from .models import *

admin.site.register(Fleet)
admin.site.register(Vehicle)
admin.site.register(VehicleInformation)
admin.site.register(VehicleImage)
admin.site.register(FleetManager)


# Register your models here.
