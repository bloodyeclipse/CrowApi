import json
from pydoc import cli
from channels.generic.websocket import AsyncWebsocketConsumer
from django.forms import model_to_dict
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user.models import User
from .models import Device, DeviceLocation, GeoFence
from django.contrib.gis.geos import Point
from .serializers import DeviceLocationSerializer


class TrackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "watchers"
        data = self.scope['url_route']['kwargs']
        client_type = data['client_type']

        if client_type == "device":
            client_uid = data['client_uid']
            device = await self.get_device(client_uid)
            if device == True:
                await self.accept()
        elif client_type == "user":
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        await self.disconnect(code=4132)

    @database_sync_to_async
    def get_device(self, uid):
        return Device.objects.filter(uid=uid).exists()

    @database_sync_to_async
    def write(self, data):
        loc = data['data']
        p = Point(loc['lat'], loc['lon'])
        device = Device.objects.get(uid=data['device'])
        containing_fence = GeoFence.objects.filter(geometry__covers=p).first()
        in_fence = containing_fence == device.geofence
        msg = {
            'location': p,
            'speed': loc['speed'],
            'sat_count': loc['SAT'],
            'in_geofence': in_fence
        }
        msg['device'] = device
        d = DeviceLocation(**msg)
        device.last_location = p
        device.save()
        d.save()
        return True

    @database_sync_to_async
    def user_exists(self, uid):
        return User.objects.filter(uid=uid).exists()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.write(data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast',
                'message': text_data
            }
        )

    async def broadcast(self, message):
        data = message['message']
        await self.send(text_data=data)
