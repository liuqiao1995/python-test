from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter, ProtocolTypeRouter
from django.urls import path

from .consumers import EchoConsumer, NoPasswordConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path(r"ws/", EchoConsumer),
            path(r"no_password/", NoPasswordConsumer),
        ])
    )
})
