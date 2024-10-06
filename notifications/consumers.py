import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import NotificationSystem
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtén el usuario que se está conectando
        self.user = self.scope["user"]
        
        # Verifica si el usuario está autenticado
        if not self.user.is_authenticated:
            # Rechaza la conexión si no está autenticado
            await self.close()
            return

        # Define un canal/grupo único para el usuario
        self.channel_group = f"user_{self.user.id}"

        # Unirse al grupo del usuario
        await self.channel_layer.group_add(self.channel_group, self.channel_name)

        # Aceptar la conexión
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo del usuario
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)

    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        receiver_id = text_data_json["receiver"]  # id del receptor

        try:
            receiver = await self.get_user(receiver_id)
        except User.DoesNotExist:
            # Maneja el caso cuando el usuario receptor no existe
            return

        notification = await self.create_notification(
            sender=self.user, receiver=receiver, message=message
        )

        # Envía la notificación al grupo del receptor
        await self.channel_layer.group_send(
            f"user_{receiver.id}",  # Canal del receptor
            {"type": "notification.message", "message": message}
        )

    # Receive message from room group
    async def notification_message(self, event):
        message = event["message"]

        # Enviar el mensaje al WebSocket del usuario
        await self.send(text_data=json.dumps({"message": message}))

    @staticmethod
    async def get_user(user_id):
        return await User.objects.aget(pk=user_id)

    @staticmethod
    async def create_notification(sender, receiver, message):
        return await NotificationSystem.objects.acreate(
            sender=sender, receiver=receiver, message=message
        )