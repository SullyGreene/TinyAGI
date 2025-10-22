# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/tools/weather_tool.py

import requests
from .base_tool import BaseTool
from geopy.geocoders import Nominatim

class WeatherTool(BaseTool):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "WeatherTool"
        self.description = "A tool to get the current weather for a given city."
        self.geolocator = Nominatim(user_agent="TinyAGI")

    def execute(self, city: str):
        """Gets the current weather for a given city."""
        try:
            location = self.geolocator.geocode(city)
            if not location:
                return f"Could not find location for {city}."

            url = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current_weather=true"
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
            return f"The current temperature in {city} is {weather_data['current_weather']['temperature']}°C."
        except Exception as e:
            return f"Error getting weather data: {e}"