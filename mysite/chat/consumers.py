#chat/consumers.py

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json

#同步 需要同步把下划线删除，并注释异步的类
class _ChatConsumer(WebsocketConsumer):

    def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name

        #join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        #接受WebSocket连接
        #如果不在connect()方法中调用accept(),则拒绝并关闭连接
        self.accept()

    #close websocket
    def disconnect(self, code):
        print('disconnect')
        #leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    #receive message from Websocket
    def receive(self, text_data=None, bytes_data=None):
        print('receive')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        #send message to room group
        #将事件发送给组
        #事件具有‘type’与应该在接收事件的使用者上调用的方法名称相对应的特殊键
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    #Receive message from room group
    def chat_message(self,event):
        print('chat_message')
        message = event['message']

        #send message to websocket
        self.send(text_data=json.dumps({
            'message': message
        }))


#异步
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print('connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' %self.room_name

        #join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        #接受WebSocket连接
        #如果不在connect()方法中调用accept(),则拒绝并关闭连接
        await self.accept()

    #close websocket
    async def disconnect(self, code):
        print('disconnect')
        #leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    #receive message from Websocket
    async def receive(self, text_data=None, bytes_data=None):
        print('receive')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        #send message to room group
        #将事件发送给组
        #事件具有‘type’与应该在接收事件的使用者上调用的方法名称相对应的特殊键
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    #Receive message from room group
    async def chat_message(self,event):
        print('chat_message')
        message = event['message']

        #send message to websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

