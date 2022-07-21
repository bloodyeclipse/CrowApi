from rest_framework import serializers
from .models import *

from package.serializers import PackageSerializer

class DeviceSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    class Meta:
        model = Device
        fields = ['uid','code','description','package','mac_address']

class DeviceLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLocation
        fields = '__all__'