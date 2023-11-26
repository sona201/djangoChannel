import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync

from chat.tasks import tailf


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('room_group_name', self.room_group_name)
        print('channel_name', self.channel_name)
        print('username', self.scope["user"].username)

        await self.accept()

        # for item in range(100):
        #     # await self.send(text_data=json.dumps({
        #     #     'message': 'handler_aaa' + str(item)
        #     # }))
        #
        #     # Send message to room group
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'chat_message',
        #             'message': 'handler_aaa' + str(item)
        #         }
        #     )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class TailFConsumer(WebsocketConsumer):
    def connect(self):
        self.file_id = self.scope["url_route"]["kwargs"]["id"]

        self.result = tailf.delay(self.file_id, self.channel_name)

        print('connect:', self.channel_name, self.result.id)
        self.accept()

    def disconnect(self, close_code):
        # 中止执行中的Task
        self.result.revoke(terminate=True)
        print('disconnect:', self.file_id, self.channel_name)

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))