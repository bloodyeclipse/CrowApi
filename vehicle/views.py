from django.shortcuts import render
from rest_framework.permissions import (IsAuthenticated, AllowAny, )
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import *
import json
from rest_framework.generics import (GenericAPIView)
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .serializers import VehicleSerializer, FleetSerializer
from .models import *


@api_view(['GET'])
def index(request):
    return Response({
        "path": "vehicles"
    })


class VehicleView(APIView):
    @permission_classes((IsAuthenticated,))
    def get(self, request, uid):
        if Vehicle.objects.filter(uid=uid).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_204_NO_CONTENT)

    @permission_classes((IsAuthenticated,))
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_204_NO_CONTENT)
        serializer.save()
        return Response(serializer.data)


class FleetView(APIView):
    @permission_classes((IsAuthenticated,))
    def get(self, request, uid):
        if not Fleet.objects.filter(uid=uid).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        fleet = Fleet.objects.get(uid=uid)
        serializer = FleetSerializer(instance=fleet, many=False)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(serializer.data)
