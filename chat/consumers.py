import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatGroup, GroupMessage
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async
from . import translator as tl

class ChatroomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        
        try:
            self.chatroom = await sync_to_async(ChatGroup.objects.get)(group_name=self.chatroom_name)
        except ChatGroup.DoesNotExist:
            await self.close()
            return
        
        await self.channel_layer.group_add(self.chatroom_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chatroom_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            body = text_data_json['body']
            language = text_data_json['language']

            # Crear mensaje de manera asíncrona
            message = await sync_to_async(GroupMessage.objects.create)(
                body=body,
                author=self.user,
                group=self.chatroom
            )

            await self.channel_layer.group_send(
                self.chatroom_name,
                {
                    'type': 'message_handler',
                    'message_id': message.id,
                    'language':language
                }
            )

        except Exception as e:
            print("Error en receive:", e)
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def message_handler(self, event):
        try:
            message_id = event['message_id']

            # Obtener el mensaje y los datos relacionados de manera asíncrona
            language = event['language']
            message = await sync_to_async(GroupMessage.objects.get)(pk=message_id)
            author_username = await sync_to_async(lambda: message.author.username)()
            message = await sync_to_async(tl.llm_basic)(language, message.body)

            data_context = {
                'message': message,
                'author': author_username,
            }

            # Enviar mensaje a través del WebSocket
            await self.send(text_data=json.dumps(data_context))

        except GroupMessage.DoesNotExist:
            print("Error en message_handler: Message not found")
            await self.send(text_data=json.dumps({"error": "Message not found"}))

        except Exception as e:
            print("Error en message_handler:", e)
            await self.send(text_data=json.dumps({"error": str(e)}))
