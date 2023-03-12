import os
from django.urls import re_path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from user.consumers import *
from django.urls import re_path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rdjango1.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
              
              re_path(r'^ws/(?P<room_name>\w+)/$', TextRoomConsumer.as_asgi()),
              re_path(r'^ws/(?P<room_name>\w+)$', NotifyRoomConsumer.as_asgi()),
            ])
)
),
})