from django.shortcuts import render, redirect
from .models import SensorData
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import SensorDataSerializer

from datetime import datetime
import logging

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 

def dashboard(request):
    return render(request, 'stats/dashboard.html', {})

def chart_data(request):
    data_items = SensorData.objects.order_by('-timestamp')[:30]  # Get the 30 most recent SensorData objects
    pH_data = list(reversed([float(item.pH_value) for item in data_items])) # list of pH values
    temperature_data = list(reversed([float(item.temperature) for item in data_items]))# List of temperatures 
    tds_data= list(reversed([float(item.tds_value) for item in data_items])) # List of tds values
    chart_labels = list(reversed([f"{item.timestamp.strftime('%H:%M:%S')}" for item in data_items])) #modifying the timestamp in the format '%H:%M:%S'

    return JsonResponse({
        "pH_data": pH_data,
        "temperature_data" : temperature_data,
        "tds_data" : tds_data,
        "chartLabels": chart_labels,
    })

logger = logging.getLogger(__name__)


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def perform_create(self, serializer):
        try:
            instance = serializer.save()

            pH_value = float(instance.pH_value) #Extracting the pH value
            temperature = float(instance.temperature) #Extracting the temperature
            tds_value = float(instance.tds_value) #Extracting the TDS

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)( #Sending data through the web socket
                "my_app_SensorData", # The room group name 
                {   'type': 'SensorData_message',  #calling the method SensorData
                    'pH_value': pH_value, 
                    'temperature': temperature,
                    'tds_value': tds_value,
                    'timestamp' : datetime.now().strftime("%H:%M:%S")
                  }
            )
        except Exception as e:
            logger.error(f"Error in perform_create: {str(e)}") # Log the error message
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500) # Return a JSON response with a generic error message and 500 status code
