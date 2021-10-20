# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import CommentSerializer, CommentSerializer1, UserSerializer1
from channels.db import database_sync_to_async
from . import models

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
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
        # print(text_data)
        card= text_data_json['card']
        message = text_data_json['message']
        commented_by = int(self.scope['user'].id)

        data={
            'User': commented_by,
            'Card': card,
            'Comment':message
        }

        # Send message to room group

        # print(data)

        userData_to_send= await self.save_comment(data)
        # await self.save_comment(data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': data['Comment'],
                'data': userData_to_send
            }
        )

    @database_sync_to_async
    def save_comment(self, data):
        
        User= models.User.objects.get(id=data['User'])
        # print(User)
        Card= models.Card.objects.get(id=data['Card'])   
        comment= models.Comment.objects.create(User= User,Card=Card, Comment=data['Comment'])

        CommentSerializer_data= CommentSerializer1(comment)
        print(CommentSerializer_data.data)

        return CommentSerializer_data.data

        # comment = CommentSerializer(data=data)
        # print(comment)
        # comment.is_valid(raise_exception=True)
        
        # return comment


    # Receive message from room group
    async def chat_message(self, event):
        print(event)
        message = event['message']
        data= event['data']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': data
            
        }))