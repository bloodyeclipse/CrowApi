from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE,
                                   HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import Group
import json
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token


@api_view(['GET'])
@permission_classes((AllowAny,))
def index(request):
    return Response({'path': 'auth/'})
