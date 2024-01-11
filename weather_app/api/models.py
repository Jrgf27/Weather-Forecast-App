"""Weather model"""

from django.db import models
from django.conf import settings

class WeatherData(models.Model):
    """Item Category model class"""

    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length = 8, choices = settings.WEATHER_TYPE_CHOICES)
    time_requested = models.DateTimeField(auto_now_add = True)
    weather_data= models.JSONField()

    # def __str__(self) -> str:
    #     return str(self.name)
