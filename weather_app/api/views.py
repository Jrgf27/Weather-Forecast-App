# pylint: disable=relative-beyond-top-level
# pylint: disable=line-too-long
"""View functions for weather application"""
from datetime import timedelta

from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView
from django.http.response import HttpResponse

import requests

from .forms import WeatherAPICallForm
from .models import WeatherData

# Create your views here.
class HomePage(TemplateView):
    """Weather Application home page class"""
    def get(self, request, *args, **kwargs):
        """Main page view function"""
        print(settings.API_KEY)
        form = WeatherAPICallForm()
        context = {"form":form}
        return render(request, 'home.html', context=context)

    def post(self, request):
        """POST method for requesting weather API data"""
        form = WeatherAPICallForm(request.POST)
        if form.is_valid():

            latitude = round(form.cleaned_data['latitude'], 2)
            longitude = round(form.cleaned_data['longitude'], 2)
            data_type = form.cleaned_data['type']

            weather_data = (
                WeatherData.objects
                .filter(latitude=latitude, longitude=longitude, type=data_type)
                .order_by('-time_requested')
                .first()
            )

            api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={settings.API_KEY}"

            if weather_data:

                current_time = timezone.now()
                time_difference = current_time-weather_data.time_requested

                if time_difference >= timedelta(minutes=settings.TIME_PER_REQUEST):
                    print("sending request")
                    api_request = requests.get(api_url, timeout=20)

                    if api_request.status_code == 200:
                        data = api_request.json()
                        weather_data.weather_data = data[data_type]
                        weather_data.time_requested = timezone.now()
                        weather_data.save()
                    else:
                        return HttpResponse('Unable to connect to weather API')

            else:

                api_request = requests.get(api_url, timeout=20)
                if api_request.status_code == 200:
                    data = api_request.json()
                    try:
                        weather_data = WeatherData(
                            latitude = latitude,
                            longitude = longitude,
                            type = data_type,
                            weather_data = data[data_type],
                        )
                        weather_data.save()
                    except KeyError:
                        return HttpResponse('API did not have data for that current weather type')
                else:
                    return HttpResponse('Unable to connect to weather API')

            context = {
                "weather_data" : weather_data.weather_data,
                "data_type" : data_type,
                }

            return render(request, 'partials/weather_data.html', context=context)

        return HttpResponse('Invalid form submitted!')
