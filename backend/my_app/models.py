from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class SensorData(models.Model):
    temperature = models.DecimalField(max_digits=100,decimal_places=2,default="0")
    pH_value = models.DecimalField(max_digits=100,decimal_places=2,default="0")
    tds_value = models.DecimalField(max_digits=100,decimal_places=2,default="0")
    timestamp = models.DateTimeField(auto_now_add=True)  # Add a timestamp field