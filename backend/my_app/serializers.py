from rest_framework import serializers
from .models import DataItem , pH_value

class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = ['statistic', 'value', 'timestamp']

class pH_valueSerializer(serializers.ModelSerializer):
    class Meta:
        model = pH_value
        fields = ['value', 'timestamp']

