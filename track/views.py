from ast import List
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated, AllowAny, )
from rest_framework.generics import ListAPIView
from .serializers import *
# Create your views here.

@api_view(['GET'])
def index(request):
    return Response({"view": "TRACK"})

class Devices(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceLocationHistory(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get_query(self,request):
        return  DeviceLocation.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = DeviceLocationSerializer