"""
Data models for the Fogcast MCP Server.
"""

from .weather_data import WeatherData, ForecastData, CurrentWeatherData
from .api_response import APIResponse

__all__ = ['WeatherData', 'ForecastData', 'CurrentWeatherData', 'APIResponse']
