"""
Fogcast API client for weather data integration.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .http_client import HTTPClient
from ..models.weather_data import ForecastData, CurrentWeatherData
from ..models.api_response import APIResponse
from ..config import config


logger = logging.getLogger(__name__)


class FogcastClient:
    """Client for interacting with the Fogcast API."""
    
    def __init__(self):
        """Initialize Fogcast client."""
        self.http_client = HTTPClient(
            base_url=config.fogcast_base_url,
            timeout=config.fogcast_timeout
        )
    
    async def get_available_models(self) -> APIResponse:
        """
        Get available forecast models.
        
        Returns:
            APIResponse containing list of available models
        """
        try:
            logger.info("Fetching available forecast models")
            response_data = await self.http_client.get('/models')
            
            # Extract models from response
            models = response_data if isinstance(response_data, list) else response_data.get('data', [])
            
            return APIResponse.success_response(
                data=models,
                message=f"Retrieved {len(models)} available models"
            )
            
        except Exception as e:
            logger.error(f"Error fetching available models: {e}")
            return APIResponse.error_response(
                error=str(e),
                message="Failed to fetch available models"
            )
    
    async def get_forecasts(self, datetime_str: str, model_id: str) -> APIResponse:
        """
        Get weather forecasts for a specific model and datetime.
        
        Args:
            datetime_str: Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ
            model_id: ID of the forecast model
            
        Returns:
            APIResponse containing forecast data
        """
        try:
            logger.info(f"Fetching forecasts for model {model_id} at {datetime_str}")
            
            params = {
                'datetime': datetime_str,
                'model_id': model_id
            }
            
            response_data = await self.http_client.get('/forecasts', params=params)
            
            # Process forecast data
            forecasts = self._process_forecast_data(response_data, model_id)
            
            return APIResponse.success_response(
                data=forecasts,
                message=f"Retrieved {len(forecasts)} forecast entries"
            )
            
        except Exception as e:
            logger.error(f"Error fetching forecasts: {e}")
            return APIResponse.error_response(
                error=str(e),
                message="Failed to fetch forecasts"
            )
    
    async def get_current_forecast(self, model_id: str) -> APIResponse:
        """
        Get the current forecast for a specific model.
        
        Args:
            model_id: ID of the forecast model
            
        Returns:
            APIResponse containing current forecast data
        """
        try:
            logger.info(f"Fetching current forecast for model {model_id}")
            
            params = {'model_id': model_id}
            response_data = await self.http_client.get('/current-forecast', params=params)
            
            # Process forecast data
            forecasts = self._process_forecast_data(response_data, model_id)
            
            return APIResponse.success_response(
                data=forecasts,
                message=f"Retrieved current forecast for model {model_id}"
            )
            
        except Exception as e:
            logger.error(f"Error fetching current forecast: {e}")
            return APIResponse.error_response(
                error=str(e),
                message="Failed to fetch current forecast"
            )
    
    async def get_live_data(self) -> APIResponse:
        """
        Get current live weather and water level data.
        
        Returns:
            APIResponse containing live weather data
        """
        try:
            logger.info("Fetching live weather data")
            response_data = await self.http_client.get('/actual/live-data')
            
            # Process live data
            live_data = self._process_live_data(response_data)
            
            return APIResponse.success_response(
                data=live_data,
                message="Retrieved current live weather data"
            )
            
        except Exception as e:
            logger.error(f"Error fetching live data: {e}")
            return APIResponse.error_response(
                error=str(e),
                message="Failed to fetch live weather data"
            )
    
    def _process_forecast_data(self, response_data: Any, model_id: str) -> List[Dict[str, Any]]:
        """
        Process raw forecast data from API response.
        
        Args:
            response_data: Raw response data from API
            model_id: Model ID for the forecasts
            
        Returns:
            List of processed forecast data dictionaries
        """
        forecasts = []
        
        # Handle different response formats
        if isinstance(response_data, list):
            data_list = response_data
        elif isinstance(response_data, dict):
            data_list = response_data.get('data', [response_data])
        else:
            data_list = [response_data]
        
        for item in data_list:
            try:
                forecast_dict = {
                    'model_id': model_id,
                    'timestamp': item.get('timestamp', item.get('datetime')),
                    'temperature': item.get('temperature'),
                    'humidity': item.get('humidity'),
                    'pressure': item.get('pressure'),
                    'wind_speed': item.get('wind_speed'),
                    'wind_direction': item.get('wind_direction'),
                    'visibility': item.get('visibility'),
                    'precipitation': item.get('precipitation'),
                    'fog_probability': item.get('fog_probability', item.get('fog_forecast'))
                }
                forecasts.append(forecast_dict)
            except Exception as e:
                logger.warning(f"Error processing forecast item: {e}")
                continue
        
        return forecasts
    
    def _process_live_data(self, response_data: Any) -> List[Dict[str, Any]]:
        """
        Process raw live data from API response.
        
        Args:
            response_data: Raw response data from API
            
        Returns:
            List of processed live data dictionaries
        """
        live_data = []
        
        # Handle different response formats
        if isinstance(response_data, list):
            data_list = response_data
        elif isinstance(response_data, dict):
            data_list = response_data.get('data', [response_data])
        else:
            data_list = [response_data]
        
        for item in data_list:
            try:
                live_dict = {
                    'source': item.get('source', 'unknown'),
                    'station_id': item.get('station_id'),
                    'timestamp': item.get('timestamp', item.get('datetime')),
                    'temperature': item.get('temperature'),
                    'humidity': item.get('humidity'),
                    'pressure': item.get('pressure'),
                    'wind_speed': item.get('wind_speed'),
                    'wind_direction': item.get('wind_direction'),
                    'visibility': item.get('visibility'),
                    'precipitation': item.get('precipitation'),
                    'water_level': item.get('water_level')
                }
                live_data.append(live_dict)
            except Exception as e:
                logger.warning(f"Error processing live data item: {e}")
                continue
        
        return live_data
    
    async def close(self):
        """Close the HTTP client connection."""
        await self.http_client.close()
