import requests
from datetime import timedelta
from django.utils import timezone
from .models import WeatherData
from django.db import models
from django.db.models import Avg, Max, Min


# OpenWeatherMap API key
API_KEY = 'c14368f9f08f71fb15ea6b78751f282d'

def fetch_weather_data(city):
    # Checking if there's weather data for the city within the last 5 minutes
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    recent_weather_data = WeatherData.objects.filter(city=city, timestamp__gte=five_minutes_ago).last()
    
    if recent_weather_data:
        # If recent data exists, don't fetch new data
        return recent_weather_data
    else:
        # Fetch fresh weather data if no recent data exists
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            weather_data = WeatherData(
                city=city,
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],  # Get wind speed
                condition=data['weather'][0]['description'],  # Get weather condition
            )
            weather_data.save()
            return weather_data 
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
            return None  #return None if there's an error


def calculate_weather_trends(city):
    """Calculates weather trends for a given city"""
    one_day_ago = timezone.now() - timedelta(hours=24)
    weather_records = WeatherData.objects.filter(city=city, timestamp__gte=one_day_ago)

    if weather_records.exists():
        # Calculate averages
        avg_temp = weather_records.aggregate(Avg('temperature'))['temperature__avg']
        avg_humidity = weather_records.aggregate(Avg('humidity'))['humidity__avg']
        
        # Calculate temperature and humidity range
        max_temp = weather_records.aggregate(Max('temperature'))['temperature__max']
        min_temp = weather_records.aggregate(Min('temperature'))['temperature__min']
        max_humidity = weather_records.aggregate(Max('humidity'))['humidity__max']
        min_humidity = weather_records.aggregate(Min('humidity'))['humidity__min']
        
        # Calculate temperature change (difference between latest and 24-hour-old record)
        latest_record = weather_records.latest('timestamp')
        earliest_record = weather_records.earliest('timestamp')
        temp_change = latest_record.temperature - earliest_record.temperature

        return {
            'avg_temp': avg_temp,
            'avg_humidity': avg_humidity,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'max_humidity': max_humidity,
            'min_humidity': min_humidity,
            'temp_change': temp_change,
        }

    return None
