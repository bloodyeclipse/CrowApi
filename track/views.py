import datetime
import json

from django.contrib.gis.geos import Polygon
from django.forms import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE,
                                   HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN, HTTP_201_CREATED)
from rest_framework.permissions import (IsAuthenticated, AllowAny, )
from rest_framework.generics import ListAPIView
from django.contrib.gis.geos.geometry import GEOSGeometry
from rest_framework.views import APIView

from .serializers import *


# Create your views here.

@api_view(['GET'])
def index(request):
    return Response({"view": "TRACK"})


class DeviceView(APIView):
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        # print(request.data)
        data = request.data
        data['mac_address'] = request.data['mac']
        package = Package.objects.get(uid=request.data['package'])
        polygon = GeoFence.objects.get(uid=request.data['geofence'])
        fence = json.loads(GEOSGeometry(polygon.geometry).geojson)
        point = Point(tuple(fence['coordinates'][0][0]))
        data['last_location'] = point
        data['geofence'] = polygon.id
        data['package'] = package.id
        serializer = DeviceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

    @permission_classes([IsAuthenticated, ])
    def put(self, request, uid):
        data = request.data
        check = Device.objects.filter(uid=uid).exists()
        if not check:
            return Response(status=HTTP_400_BAD_REQUEST)
        device = Device.objects.get(uid=uid)

        data['package'] = Package.objects.get(uid=request.data['package']).id
        data['geofence'] = GeoFence.objects.get(uid=request.data['geofence']).id

        serializer = DeviceSerializer(instance=device, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        update = serializer.update(instance=device, validated_data=serializer.validated_data)
        update.save
        return Response(status=HTTP_200_OK)

    @permission_classes([IsAuthenticated, ])
    def delete(self, request, uid):
        if not Device.objects.filter(uid=uid).exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        device = Device.objects.get(uid=uid)
        device.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Devices(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = Device.objects.all()
    serializer_class = DeviceReadSerializer


class DeviceLocationHistory(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        ft = "%Y-%m-%d"
        st = datetime.datetime.strptime(self.kwargs['startDate'], ft)
        et = datetime.datetime.strptime(self.kwargs['endDate'], ft)
        date_range = [st, et]
        query = DeviceLocation.objects.filter(device__uid=self.kwargs['uid'], date_received__range=date_range)
        return query

    pagination_class = PageNumberPagination
    serializer_class = DeviceLocationSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listGeoFences(request):
    query = GeoFence.objects.all()
    serializer = GeofenceSerializer(instance=query, many=True)
    return Response(serializer.data)


class GeoFenceView(APIView):

    @permission_classes((IsAuthenticated,))
    def post(self, request):
        data = request.data
        submitted_geometry = []
        for g in data['geometry']:
            submitted_geometry.append(tuple(g))
        geometry = tuple(submitted_geometry)
        data['geometry'] = Polygon(geometry)
        serializer = GeofenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)

    @permission_classes((IsAuthenticated,))
    def put(self, request, uid):
        if not GeoFence.objects.filter(uid=uid).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        data = request.data
        fence = GeoFence.objects.get(uid=uid)
        submitted_geometry = []
        for g in data['geometry']:
            submitted_geometry.append(tuple(g))
        geometry = tuple(submitted_geometry)
        data['geometry'] = Polygon(geometry)
        serializer = GeofenceSerializer(instance=fence, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_200_OK)
