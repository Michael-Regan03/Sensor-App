from rest_framework import serializers
from .models import  SensorData

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['temperature','tds_value','pH_value', 'timestamp']

