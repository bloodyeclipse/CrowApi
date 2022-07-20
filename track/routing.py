from django.urls import  path
from .consumers import TrackConsumer

websocket_urlpatterns = [
    path('socket.io/<str:client_type>/',TrackConsumer.as_asgi()),
    path('socket.io/<str:client_type>/<uuid:client_uid>/',TrackConsumer.as_asgi()),
]