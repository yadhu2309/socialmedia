import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *


class TextRoomConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        print('text_data_json',text_data_json)
        room=text_data_json['room_name']
        message = text_data_json['text']
        sender = text_data_json['sender']

        #save in db
        if Rooms.objects.filter(id=room):

            roomid = Rooms.objects.get(id=room)
            obj = ChatMessages(room_name=roomid,sender=sender,receiver='lol',message=message)
            obj.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        message = event['message']
        sender = event['sender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))



class NotifyRoomConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        print('text_data_json',text_data_json)
        # room=text_data_json['room_name']
        message = text_data_json['text']
        sender = text_data_json['sender']

        #save in db
        # if Rooms.objects.filter(id=room):

        #     roomid = Rooms.objects.get(id=room)
        #     obj = ChatMessages(room_name=roomid,sender=sender,receiver='lol',message=message)
        #     obj.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    def chat_message(self, event):
        # Receive message from room group
        message = event['message']
        sender = event['sender']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))














    # def connect(self):

    #     self.room_name ='test'
    #     #  self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name ='test_consumer_group'
    #     #  'chat_%s' % self.room_name
    #     # Join room group
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #     self.accept()
    # def disconnect(self, close_code):
    #     # Leave room group
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    # def receive(self, text_data):
    #     # Receive message from WebSocket
    #     text_data_json = json.loads(text_data)
    #     text = text_data_json['text']
    #     sender = text_data_json['sender']
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': text,
    #             'sender': sender
    #         }
    #     )

    # def chat_message(self, event):
    #     # Receive message from room group
    #     text = event['message']
    #     sender = event['sender']
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'text': text,
    #         'sender': sender
    #     }))
        
    # def send_notification(self,event):
    #     print('event',event)
    #     data = json.loads(event.get('value'))
    #     self.send(text_data=json.dumps({
    #         'payloads':data
    #     }))