from rest_framework import serializers

from user.Serializer import UserSerializer
from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleLog
        fields = '__all__'


class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = '__all__'


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = '__all__'


# List Serializers

class FleetListSerializer(serializers.ModelSerializer):
    manager = UserSerializer()

    class Meta:
        model = Fleet
        fields = ['uid', 'name', 'date_created', 'manager']


class VehicleFleetUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['uid']


class VehicleListSerializer(serializers.ModelSerializer):
    fleet = VehicleFleetUIDSerializer()
    driver = UserSerializer()

    class Meta:
        model = Vehicle
        fields = ['uid', 'fleet', 'brand', 'model_name', 'year', 'color', 'date_added', 'driver', 'reg_num']
