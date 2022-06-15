#this is similair to the urls.py files for views

from django.urls import re_path #use re_path due to the limiations of the path(URLRouter limitations)
from .consumers import *

#for websocket connections we start with ws/chat
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()), #regex from the url
]