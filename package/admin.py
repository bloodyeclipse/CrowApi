from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(HazardLevel)
admin.site.register(PackageType)
admin.site.register(Package)
admin.site.register(PackageImage)

