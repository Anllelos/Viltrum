import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from notifications.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Viltrum.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(  # Añade AuthMiddlewareStack para manejar la autenticación
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
