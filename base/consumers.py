from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404
from .models import Message, Room

from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_group_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()



    async def disconnect(self, message):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        action = data.get('action')

        if action == "send":
            await self.handle_send_message(data)
            print('send')
        elif action == "delete":
            await self.handle_delete_message(data)
            print('delete')


    async def handle_send_message(self, data):

        message = data['message']
        sender_username = data['sender']
        receiver_username = data['receiver']

        sender_user = await self.get_user_by_username(sender_username)

        receiver_user = await self.get_user_by_username(receiver_username)


        message_instance = await self.save_message(sender_user, message)

        await self.channel_layer.group_send(self.room_group_name, {
            "type": "send_message",
            "message": message_instance.text,
            "message_id": message_instance.pk,
            "sender": sender_username,
            "receiver": receiver_username
        })


    async def send_message(self, e):

        message = e['message']
        message_id = e['message_id']
        sender = e['sender']
        receiver = e['receiver']


        await self.send(text_data=json.dumps({
            "action": "send",
            "message": message,
            "message_id":message_id,  
            "sender": sender, 
            "receiver": receiver
            }))

        


    @database_sync_to_async
    def get_user_by_username(self, username):
        user = User.objects.get(username=username)
        if user:
            return user
        return None
    

    @database_sync_to_async
    def save_message(self, author, text):
        room = Room.objects.get(name=self.room_group_name)
        print(author, "autor")
        message = Message(room=room, author=author, text=text)
        message.save()
        
        return message
    



    async def handle_delete_message(self, data):
        message_id = data['message_id']
        
        await self.delete_message_from_db(message_id)

        # message_instance = Message.objects.get(id=message_id)
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'delete_message',
            'message_id': message_id
        })

    async def delete_message(self, e):
        message_id = e['message_id']

        await self.send(text_data=json.dumps({
            'action': 'delete',
            'message_id': message_id
        }))

    @database_sync_to_async
    def delete_message_from_db(self, id):
        Message.objects.get(id=id).delete()




class UserMessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = self.other_username

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    

    async def disconnect(self, code):
        return await super().disconnect(code)
    
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        message = data['message']
        sender = data['sender']

        receiver = data['receiver']


        await self.channel_layer.group_send(self.room_group_name, {
            "type": "send_notification",
            "message": message,
            "sender": sender,
            "receiver": receiver
        })


    async def send_notification(self, e):

        message = e['message']
        sender = e['sender']
        receiver = e['receiver']


        await self.send(text_data=json.dumps({"message": message, "sender": sender, "receiver": receiver}))
    
