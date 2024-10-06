from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/notify/<int:user_id>/', NotificationConsumer.as_asgi()),
]