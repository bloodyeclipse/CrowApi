from operator import mod
from attr import field
from rest_framework import serializers
from .models import *


class HazardLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardLevel
        fields = ['uid','name','description','color']


class PackageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields = ['uid','name','description','hazard']

class UidPackageTypeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = PackageType
        fields= ['uid']

class PackageSerializer(serializers.ModelSerializer):
    package_type = UidPackageTypeSerialiser()
    class Meta:
        model = Package
        fields = ['uid','description','name','attr','package_type']


class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = ['uid','image','description']
