from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/<str:dashboard_slug>/', consumers.DashboardConsumer.as_asgi()),
    #path(r'ws/sensor/', consumers.SensorConsumer.as_asgi()),
]