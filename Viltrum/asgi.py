"""
ASGI config for Viltrum project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

settings_module = 'Viltrum.production' if 'WEBSITE_HOSTNAME' in os.environ else 'Viltrum.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


from notifications.routing import websocket_urlpatterns as notifications_urlpatterns
from chat.routing import websocket_urlpatterns as chat_urlpatterns  

websocket_urlpatterns = notifications_urlpatterns + chat_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket":AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    )
    # Just HTTP for now. (We can add other protocols later.)
})
