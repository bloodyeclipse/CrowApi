from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('devices', Devices.as_view()),
    path('device',DeviceView.as_view()),
    path('device/<uuid:uid>',DeviceView.as_view()),
    path('report/<uuid:uid>/<str:startDate>/<str:endDate>', DeviceLocationHistory.as_view()),
    path('geofences', listGeoFences),
    path('geofence/<uuid:uid>', GeoFenceView.as_view()),
    path('geofence', GeoFenceView.as_view())
]
