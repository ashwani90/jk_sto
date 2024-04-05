
"""
ASGI entrypoint file for default channel layer.

Points to the channel layer configured as "default" so you can point
ASGI applications at "multichat.asgi:channel_layer" as their channel layer.
"""

import os
from django.urls import path
from chat.consumers import ChatConsumer
from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jkinda_stocks.settings")
application = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter([
#         path('chat/', ChatConsumer.as_asgi())
#     # you can define all your routers here
#         ])
#     # Just HTTP for now. (We can add other protocols later.)
# })
