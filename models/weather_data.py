"""
Data models for weather-related data structures.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class WeatherData:
    """Base class for weather data."""
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[float] = None
    fog_probability: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'visibility': self.visibility,
            'precipitation': self.precipitation,
            'fog_probability': self.fog_probability
        }


@dataclass
class ForecastData(WeatherData):
    """Extended weather data for forecasts."""
    model_id: str = "unknown"
    forecast_horizon: Optional[int] = None  # hours ahead
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            'model_id': self.model_id,
            'forecast_horizon': self.forecast_horizon
        })
        return base_dict


@dataclass
class CurrentWeatherData(WeatherData):
    """Extended weather data for current conditions."""
    source: str = "unknown"  # e.g., 'DWD', 'OpenMeteo', 'weather_station'
    station_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        base_dict = super().to_dict()
        base_dict.update({
            'source': self.source,
            'station_id': self.station_id
        })
        return base_dict
