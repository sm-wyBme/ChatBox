#we create a consumer which basically initiates a connection, sends and receieves messages over a channel 

import json
from channels.generic.websocket import AsyncWebsocketConsumer #making websockets async
from channels.db import database_sync_to_async #async calling from database
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'] #information about the scope
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group (add the group)
        # every channel layer has a group(related channel) and a channel(mailbox like)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.userId = self.scope['user'].id #django channels hold user

        #find Room object
        room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)

        #create new Chat-Object
        chat = Chat(
            content=message,
            user=self.scope['user'],
            room=room
        )

        await database_sync_to_async(chat.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', #calls chat_messagwe function
                'message': message,
                'userId': self.userId
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        userId = event['userId']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'userId': userId
        }))