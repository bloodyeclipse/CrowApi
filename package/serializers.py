from operator import mod
from attr import field
from rest_framework import serializers
from .models import *


class HazardLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardLevel
        fields = ['uid', 'name', 'description', 'color']


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ['uid', 'name', 'description', 'hazard']


class UidHazardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardLevel
        fields = ['uid']


class UidPackageTypeSerializer(serializers.ModelSerializer):
    hazard = UidHazardSerializer()

    class Meta:
        model = PackageType
        fields = ['uid', 'hazard']


class PackageSerializer(serializers.ModelSerializer):
    package_type = UidPackageTypeSerializer()

    class Meta:
        model = Package
        fields = ['uid', 'description', 'name', 'attr', 'package_type']


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = ['uid', 'image', 'description']
