

# The channel routing defines what channels get handled by what consumers,
# including optional matching on message attributes. In this example, we match
# on a path prefix, and then include routing from the chat module.
# channel_routing = [
#     # Include sub-routing from an app.
#     include("chat.routing.websocket_routing", path=r"^/chat"),
#     include("chat.api.routing.websocket_routing", path=r"^/api/chat"),
#     # Custom handler for message sending 
#     # Can't go in the include above as it's not got a `path` attribute to match on.
#     include("chat.routing.custom_routing"),
#     include("chat.api.routing.custom_routing"),
#     # # A default "http.request" route is always inserted by Django at the end of the routing list
#     # # that routes all unmatched HTTP requests to the Django view system. If you want lower-level
#     # # HTTP handling - e.g. long-polling - you can do it here and route by path, and let the rest
#     # # fall through to normal views.
# ]

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('chat/', ChatConsumer.as_asgi()),
    ])
})
# lets not use the websocket now
