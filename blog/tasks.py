from celery import shared_task
import requests
from django.core.cache import cache

@shared_task
def get_weather():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Karaj&appid=12efd6b12c04995d9fbf64c8f91e60f4&units=metric")
    data = response.json()

    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "wind_speed": data["wind"]["speed"],
    }

    cache.set(
        "weather_karaj",
        weather_data,
        timeout=60 * 60,
    )

    return weather_data