from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.db import database_sync_to_async
from .models import DataItem, Statistic


from random import randint
from asyncio import sleep 

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        dashboard_slug = self.scope['url_route']['kwargs']['dashboard_slug']
        self.dashboard_slug = dashboard_slug
        self.room_group_name = f'my_app_{dashboard_slug}'
        print(self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print('connection')
        await self.accept()

    async def disconnect(self, close_code):
        print(f'connection closed with code: {close_code}')
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(message)

        dashboard_slug = self.dashboard_slug

        await self.save_data_item( message, dashboard_slug)


        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'statistic_message',
            'message' : message,
        })



    async def statistic_message(self, event):
            message = event['message']

            await self.send(text_data=json.dumps({
                'message' : message,
            }))

    @database_sync_to_async
    def create_data_item(self, message, slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItem.objects.create(statistic=obj, value=message )
    
    async def save_data_item(self,message, slug):
        await self.create_data_item( message, slug)


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        try:
            for i in range(1000):
                data = {'value': randint(-20, 20)}
                await self.send(json.dumps(data))
                print("Sent:", data)
                await sleep(1)
        except Exception as e:
            print("Error sending data:", e)
        



class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Do nothing when receiving data from WebSocket client
        pass

    async def broadcast_data(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))