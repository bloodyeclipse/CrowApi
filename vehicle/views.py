from rest_framework.permissions import (IsAuthenticated, AllowAny, )
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import *
import json
from rest_framework.generics import (GenericAPIView)
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .serializers import VehicleSerializer, FleetSerializer, VehicleImageSerializer
from .models import *


@api_view(['GET'])
@permission_classes((AllowAny,))
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
        return Response(serializer.data, status=HTTP_201_CREATED)


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

    @permission_classes((IsAuthenticated,))
    def post(self, request):
        serializer = FleetSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class VehicleImages(APIView):
    @permission_classes((IsAuthenticated, AllowAny))
    def get(self, request, uid):
        if not Vehicle.objects.filter(uid=uid).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        vehicle = Vehicle.objects.get(uid=uid)
        if not VehicleImage.objects.filter(vehicle=vehicle).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        imagequeryset = VehicleImage.objects.get(vehicle=vehicle)
        serializer = VehicleImageSerializer(data=imagequeryset, many=True)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated,))
    def post(self, request, uid):
        print(request)
        print(uid)
        return Response(status=HTTP_204_NO_CONTENT)

    @permission_classes((IsAuthenticated,))
    def delete(self, request, uid):
        if not VehicleImage.objects.filter(uid=uid).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        image = VehicleImage.objects.get(uid=uid)
        image.delete()
        return Response(status=HTTP_204_NO_CONTENT)
