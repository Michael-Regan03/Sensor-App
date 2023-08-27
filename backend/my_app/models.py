from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Statistic(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("my_app:dashboard", kwargs={"slug": self.slug})
    
    @property
    def data(self):
        return self.dataitem_set.all()
    
    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class DataItem(models.Model):
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Add a timestamp field


    def __str__(self):
        return f"{self.timestamp}: {self.value}"
    

class pH_value(models.Model):
    value = models.DecimalField(max_digits=4,decimal_places=2,default="0")
    timestamp = models.DateTimeField(auto_now_add=True)  # Add a timestamp field