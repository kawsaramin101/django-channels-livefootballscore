from django.urls import re_path, path

from . import consumers

#print(re_path(r"ws/livefeed/(?P<match_id>\w+)/$", consumers.LiveFeedConsumer.as_asgi()))

websocket_urlpatterns = [
    #re_path(r"ws/livefeed/(?P<match_id>\w+)/$", consumers.LiveFeedConsumer.as_asgi()),
    path("ws/livefeed/<str:match_id>/", consumers.LiveFeedConsumer.as_asgi()),
]

