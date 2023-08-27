from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem, pH_value
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum

from rest_framework import viewsets
from .serializers import *

fake = Faker()
# Create your views here.
def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_stat = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_stat)
        return redirect("my_app:dashboard", obj.slug)
    return render(request, 'stats/main.html' , {'qs': qs} )

def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    return render(request, 'stats/dashboard.html', {
        'name': obj.name,
        'slug': obj.slug,
        'data' : obj.data
        #'user': request.user.username if request.user.username else fake.name() ,
    })

def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x["value__sum"] for x in qs]
    chart_labels = [x["owner"] for x in qs]
    return JsonResponse({
        "chartData" : chart_data,
        "chartLabels" : chart_labels,
    })

def test(request):
    return render(request, 'stats/main.html', context={'text': 'hello world'})


def chart_data_v2(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    data_items = DataItem.objects.filter(statistic=obj).order_by('-timestamp')[:30]  # Get the most recent 5 data items
    chart_data = [item.value for item in data_items]
    chart_labels = [f"{item.timestamp}: {item.timestamp}" for item in data_items]
    return JsonResponse({
        "chartData": chart_data,
        "chartLabels": chart_labels,
    })


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 

class SensorDataAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        async_to_sync(self.broadcast_data_to_websockets, data)
        return Response({'message': 'Data received and broadcasted.'}, status=status.HTTP_200_OK)
    
    def broadcast_data_to_websockets(self, data):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('sensor_group', {'type': 'broadcast.data', 'data': data})

class DataItemViewSet(viewsets.ModelViewSet):
    queryset = DataItem.objects.all()
    serializer_class = DataItemSerializer

class pH_valueViewSet(viewsets.ModelViewSet):
    queryset = pH_value.objects.all()
    serializer_class = pH_valueSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        value = float(instance.value)

        # Send data to WebSocket consumers
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "my_app_ph",
            {"type": "statistic_message", "value": value}
        )

def send_data_to_group(group_name, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(group_name, {"type": "send_data", "data": data})
   