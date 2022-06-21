from rest_framework import serializers
from .models import *


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = '__all__'