from django.shortcuts import render
from .models import WeatherData
from .utils import fetch_weather_data, calculate_weather_trends

def weather_view(request):
    city = request.GET.get('city', 'Delhi')  # default to 'Delhi'
    weather_data = fetch_weather_data(city)  # Fetching from DB or API

    if weather_data:
        # Calculate trends for the city (last 24 hours of data)
        trends = calculate_weather_trends(city)

        # Generate alerts based on weather conditions
        alert = None
        if weather_data.temperature > 40:
            alert = "Extreme heat alert! Stay indoors and keep hydrated."
        elif weather_data.wind_speed > 50:
            alert = "High wind alert! Strong winds, avoid outdoor activities."
        elif "rain" in weather_data.condition.lower() or "thunderstorm" in weather_data.condition.lower():
            alert = f"Severe weather alert: {weather_data.condition.capitalize()}! Take precautions."
        elif weather_data.temperature < 0:
            alert = "Extreme cold alert! Stay warm and indoors."

        context = {
            'weather_data': weather_data,
            'trends': trends,
            'alert': alert,
            'city': city  # Ensure the selected city is passed back to the template
        }
    else:
        # Handle the case where data could not be fetched
        context = {
            'error': f"No weather data available for {city}. Please try again later.",
            'city': city  # Ensure the selected city is passed back to the template
        }

    return render(request, 'weather/weather.html', context)
