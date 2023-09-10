from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        socket_name = 'SensorData' # Socket name
        self.room_group_name = f'my_app_{socket_name}' # Room group name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print('connection')
        await self.accept()


    async def disconnect(self, close_code):
        print(f'connection closed with code: {close_code}')
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def SensorData_message(self, event):
            pH_value = event['pH_value']
            temperature = event['temperature']
            tds_value = event['tds_value']
            timestamp = event['timestamp']
            

            await self.send(text_data=json.dumps({
                'pH_value' : pH_value,
                'temperature' : temperature,
                'tds_value' : tds_value,
                'timestamp' : timestamp,
            }))

