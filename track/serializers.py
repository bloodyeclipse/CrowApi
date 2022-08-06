from django.contrib.gis.forms import PolygonField
from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos.polygon import GEOSGeometry, Polygon
from .models import *

from package.serializers import PackageSerializer


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class GeofenceUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoFence
        fields = ['uid',]


class DeviceReadSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    last_location = Point()
    geofence = GeofenceUIDSerializer()

    class Meta:
        model = Device
        fields = ['uid', 'code', 'description', 'package', 'mac_address', 'last_location', 'geofence']
        extra_kwargs = {
            'last_location': {
                'read_only': True
            },
            'package': {
                'read_only': True
            },
            'geofence': {
                'read_only': True
            }
        }


class DeviceUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['uid']


class DeviceLocationSerializer(serializers.ModelSerializer):
    location = PointField()
    device = DeviceUIDSerializer()

    class Meta:
        model = DeviceLocation
        fields = ['uid', 'location', 'in_geofence', 'speed', 'sat_count', 'device', 'date_received']
        extra_kwargs = {
            'location': {
                'read_only': True
            }
        }


class GeofenceSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GeoFence
        geo_field = 'geometry'
        fields = '__all__'
