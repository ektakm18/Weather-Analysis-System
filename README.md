# Weather Analysis System

This repository contains a Django-based web application that fetches real-time weather data from the OpenWeatherMap API, processes the data, and provides insights, including weather trends and extreme weather alerts for selected cities.

## Features

- Fetches and displays real-time weather data (temperature, humidity, wind speed, etc.).
- Provides weather alerts for extreme conditions (heat, storms, etc.).
- Displays weather trends, such as average temperature and humidity over the last 24 hours.
- Supports city selection for customized weather reports.

## Technologies Used

- **Backend**: Django 5.1.1
- **Frontend**: HTML, CSS
- **Database**: SQLite (in development), PostgreSQL (recommended for production)
- **API**: OpenWeatherMap API
- **Web Server**: Gunicorn (for production)
