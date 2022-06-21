from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('<uuid:uid>/', VehicleView.as_view(), name="Get car"),
    path('fleet/<uuid:uid>', FleetView.as_view(), name="Get Fleet"),
]
