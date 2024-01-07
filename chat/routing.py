from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path('ticket/detail/(?P<slug>[-\w]+)/chat/$', consumers.ChatConsumer.as_asgi()),
]