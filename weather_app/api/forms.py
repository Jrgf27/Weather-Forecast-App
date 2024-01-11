"""Form used in weather app"""
from django import forms
from django.conf import settings

class WeatherAPICallForm(forms.Form):
    """Class with Item Category form"""
    latitude = forms.FloatField(max_value = 90, min_value = -90)
    longitude = forms.FloatField(max_value = 180, min_value = -180)
    type = forms.ChoiceField(choices = settings.WEATHER_TYPE_CHOICES)
