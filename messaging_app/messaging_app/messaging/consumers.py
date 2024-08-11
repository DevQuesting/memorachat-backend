# messaging/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope['url_route']['kwargs']['chat_name']
        self.chat_group_name = f'chat_{self.chat_name}'

        # Join the chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']
        sender = text_data_json['sender']

        if event_type == 'typing':
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_typing',
                    'sender': sender,
                }
            )

    # Handle typing event
    async def chat_typing(self, event):
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': sender,
        }))
