from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated, AllowAny, )
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.decorators import *
import json
from rest_framework.generics import (GenericAPIView, ListAPIView, )
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from user.decorators import allowed_groups
from .serializers import *
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

    @permission_classes([IsAuthenticated, ])
    def put(self, request, uid):

        if not Vehicle.objects.filter(uid=uid).exists():
            return Response(status=HTTP_204_NO_CONTENT)

        if 'driver' in request.data:

            if not User.objects.filter(uid=request.data['driver']).exists():
                return  Response(status=HTTP_403_FORBIDDEN)
            request.data['driver'] = User.objects.get(uid=request.data['driver']).id

        if 'fleet' in request.data:
            if not Fleet.objects.filter(uid=request.data['fleet']).exists():
                return Response(status=HTTP_403_FORBIDDEN)
            request.data['fleet'] = Fleet.objects.get(uid=request.data['fleet']).id

        vehicle = Vehicle.objects.get(uid=uid)
        serializer = VehicleSerializer(instance=vehicle, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_202_ACCEPTED)

    @permission_classes((IsAuthenticated,))
    # @allowed_groups(['Manager'])
    def post(self, request):
        data = request.data
        if not Fleet.objects.filter(uid=data['fleet']).exists():
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        fleet = Fleet.objects.get(uid=data['fleet'])
        data['fleet'] = fleet.id
        serializer = VehicleSerializer(data=data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_204_NO_CONTENT)
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
    @allowed_groups(['Manager'])
    def delete(self, request, uid):
        if not VehicleImage.objects.filter(uid=uid).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        image = VehicleImage.objects.get(uid=uid)
        image.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class VehicleListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = Vehicle.objects.all()
    serializer_class = VehicleListSerializer


class FleetListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    queryset = Fleet.objects.all()
    serializer_class = FleetListSerializer


class FleetManagerListView(ListAPIView):
    queryset = User.objects.filter(groups__name='manager')
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer


class FleetManagerView(APIView):
    @permission_classes([IsAuthenticated])
    def put(self, request, uid):
        if not Fleet.objects.filter(uid=uid).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        if not User.objects.filter(uid=request.data['uid']).exists():
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        fleet = Fleet.objects.get(uid=uid)
        manger = User.objects.get(uid=request.data['uid'])
        fleet.manager = manger.id
        fleet.save()
        return Response(status=HTTP_200_OK)


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

        data = request.data

        if not User.objects.filter(uid=data['manager']).exists():
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        manager = User.objects.get(uid=data['manager'])
        data['manager'] = manager.id

        serializer = FleetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)


class DriverListView(ListAPIView):
    queryset = User.objects.filter(groups__name="driver")
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
