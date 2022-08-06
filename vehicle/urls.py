from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),

    path('fleets', FleetListView.as_view(), name="Get Fleet List"),
    path('fleet/<uuid:uid>', FleetView.as_view(), name="Get Fleet"),
    path('fleet', FleetView.as_view()),

    path('vehicles', VehicleListView.as_view(), name="Get Vehicle List"),
    path('vehicle/<uuid:uid>', VehicleView.as_view(), name="Read-Update-Delete Vehicle View"),
    path('vehicle', VehicleView.as_view(), name="Create Vehicle"),

    path('drivers', DriverListView.as_view(), name="List Drivers"),
    path('managers', FleetManagerListView.as_view(), name="List Managers"),
    # path('manager/<uuid:uid>',ManagerView.as_view(),name="Read-Update-Delete Manager View"),
    # path('manager',FleetManagerView.as_view(),name='Create Manager View'),
]
