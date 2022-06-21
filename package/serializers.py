from rest_framework import serializers
from .models import *


class HazardLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardLevel
        fields = '__all__'


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        models = PackageType
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        models = Package
        fields = '__all__'


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        models = PackageImage
        fields = '__all__'
