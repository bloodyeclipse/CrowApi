from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('devices',Devices.as_view())
]