from django.urls import re_path
from .consumers import ChatConsumer, UserMessageConsumer


ws_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/messages/(?P<username>\w+)/$", UserMessageConsumer.as_asgi())

]