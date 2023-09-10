from django.urls import path, include
from .views import dashboard, chart_data, SensorDataViewSet
from rest_framework import routers

app_name = 'my_app'

router = routers.DefaultRouter()

router.register('sensorData', SensorDataViewSet, basename="sensorData" ) 

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('chart/', chart_data, name='chart'),
    path('api/', include(router.urls)),
]