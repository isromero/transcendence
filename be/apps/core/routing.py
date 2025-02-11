from django.urls import re_path
from .consumers import PongConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/$', PongConsumer.as_asgi()),
]
