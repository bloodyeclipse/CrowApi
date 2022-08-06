from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, )
from rest_framework.response import Response
from rest_framework.status import *
from user.decorators import allowed_groups
from rest_framework.decorators import *
from rest_framework.views import APIView
from .serializers import *
from .models import *
from user.decorators import allowed_groups


@api_view(['GET'])
def index(request):
    return Response({"path": "packages/"})


class PackageTypeList(ListAPIView):
    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    permission_classes = (AllowAny, IsAuthenticated,)
    pagination_class = PageNumberPagination


class PackageTypeView(APIView):
    @permission_classes((IsAuthenticatedOrReadOnly,))
    def get(self, request, uid):
        if not PackageType.objects.filter(uid=uid).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        p_type = PackageType.objects.get(uid=uid)
        serializer = PackageTypeSerializer(p_type)
        return Response(serializer.data)

    @permission_classes((IsAuthenticated,))
    @allowed_groups(['Admin', 'Manager'])
    def post(self, request):
        serializer = PackageTypeSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


class PackageListUncategorized(ListAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all().order_by('-date_added')
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)


class PackageListCategorized(ListAPIView):
    def get_queryset(self):
        type_uid = self.kwargs['uid']
        if not PackageType.objects.filter(uid=type_uid).exists():
            return []
        p_type = PackageType.objects.get(uid=type_uid).order_by('-date_added')
        if not Package.objects.filter(package_type=p_type).exists():
            return []
        return Package.objects.filter(package_type=p_type)

    serializer_class = PackageSerializer
    authentication_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class PackageView(APIView):
    @permission_classes((AllowAny,))
    def get(self, request, uid):
        if not Package.objects.filter(uid=uid).exists():
            return Response(status=HTTP_404_NOT_FOUND)
        p = Package.objects.get(uid=uid)
        serializer = PackageSerializer(p)
        return Response(serializer.data)

    @permission_classes((AllowAny,))
    @allowed_groups(['admin', 'manager'])
    def post(self, request):
        serializer = PackageSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)


class PackageImages(APIView):
    @permission_classes((IsAuthenticated,))
    @allowed_groups(['Manager'])
    def post(request):
        print(request)
        return Response({})

    @permission_classes((IsAuthenticated,))
    def get(self, request, uid):
        pack = Package.objects.get(uid=uid)
        if not PackageImage.objects.filter(package=pack).exists():
            return Response(status=HTTP_204_NO_CONTENT)
        images = PackageImage.objects.filter(package=pack)
        serializer = PackageImageSerializer(instance=images, many=True)
        return Response(serializer.data)


class HarzardsView(APIView):
    @permission_classes([IsAuthenticated])
    @allowed_groups(['Manager', 'Admin'])
    def post(self, request):
        serializer = HazardLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @permission_classes((IsAuthenticated))
    def get(self, request):
        hazardLevels = HazardLevel.objects.all()
        serializer = HazardLevelSerializer(instance=hazardLevels, many=True)
        return Response(serializer.data)
