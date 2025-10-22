# MIT License
# Copyright (c) 2025 Sully Greene
# Repository: https://github.com/SullyGreene
# Profile: https://x.com/@SullyGreene

# TinyAGI/plugins/weather_plugin.py

from .base_plugin import BasePlugin

class WeatherPlugin(BasePlugin):
    def __init__(self, config=None):
        super().__init__(config)
        self.name = "WeatherPlugin"
        self.description = "A plugin to get the current weather for a given city."

    def execute(self, agent, tool, input_data, options, stream=False):
        city = input_data.get('city')
        if not city:
            return "I need a city to get the weather for."

        return agent.act(tool, city=city)
