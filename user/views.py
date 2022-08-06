from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE,
                                   HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN, HTTP_201_CREATED)
from rest_framework.views import APIView
from rest_framework import generics, mixins
from django.contrib.auth.models import Group

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from .Serializer import UserSerializer
from django.forms.models import model_to_dict

'''
ACCOUNT CONVERSION START
Convert and instance of the account model to a dictionary
exculde the following fields ['password','user_permissions','is_superuser','is_staff','last_login']
'''


def acc_to_dict(account=None):
    account._mutable = False
    u = model_to_dict(account, exclude=['id', 'password', 'user_permissions', 'is_superuser', 'is_staff', 'last_login'])
    u['profile_img'] = account.profile_img.url
    u['date_joined'] = str(account.date_joined)
    return u


'''
ACCOUNT CONVERSION END
'''


# Signup View
@api_view(['POST'])
def signUp(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def AuthUser(request):
    # user = acc_to_dict(request.user)
    user = UserSerializer(instance=request.user, many=False)
    return Response(user.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def AuthOverview(request):
    sheet = {
        "Account": {
            "signIn": "signIn",
            "signUp": "signUp",
        }
    }
    return Response(sheet)

