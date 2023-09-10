from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/SensorData/', consumers.DashboardConsumer.as_asgi()),
]