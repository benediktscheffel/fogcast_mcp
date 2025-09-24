"""
MCP tools for weather forecast data access.
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

from ..integration.fogcast_client import FogcastClient
from ..models.api_response import APIResponse


logger = logging.getLogger(__name__)


class ForecastTools:
    """MCP tools for accessing weather forecast data."""
    
    def __init__(self, fogcast_client: FogcastClient):
        """
        Initialize forecast tools.
        
        Args:
            fogcast_client: Fogcast API client instance
        """
        self.fogcast_client = fogcast_client
    
    async def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available forecast models.
        
        Returns:
            Dictionary containing available forecast models
        """
        try:
            logger.info("Getting available forecast models")
            
            response = await self.fogcast_client.get_available_models()
            
            if not response.success:
                return {
                    'success': False,
                    'error': response.error,
                    'message': response.message
                }
            
            return {
                'success': True,
                'data': {
                    'models': response.data,
                    'count': len(response.data)
                },
                'message': f"Retrieved {len(response.data)} available models"
            }
            
        except Exception as e:
            logger.error(f"Error getting available models: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve available models'
            }
    
    async def get_forecast(self, model_id: str, datetime_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Get weather forecast for a specific model and datetime.
        
        Args:
            model_id: ID of the forecast model
            datetime_str: Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)
            
        Returns:
            Dictionary containing forecast data
        """
        try:
            logger.info(f"Getting forecast for model {model_id} at {datetime_str or 'current time'}")
            
            if datetime_str:
                # Get forecast for specific datetime
                response = await self.fogcast_client.get_forecasts(datetime_str, model_id)
            else:
                # Get current forecast
                response = await self.fogcast_client.get_current_forecast(model_id)
            
            if not response.success:
                return {
                    'success': False,
                    'error': response.error,
                    'message': response.message
                }
            
            return {
                'success': True,
                'data': {
                    'model_id': model_id,
                    'forecast_datetime': datetime_str,
                    'forecasts': response.data,
                    'count': len(response.data)
                },
                'message': f"Retrieved {len(response.data)} forecast entries for model {model_id}"
            }
            
        except Exception as e:
            logger.error(f"Error getting forecast: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve forecast data'
            }
    
    async def get_current_forecast(self, model_id: str) -> Dict[str, Any]:
        """
        Get current forecast for a specific model.
        
        Args:
            model_id: ID of the forecast model
            
        Returns:
            Dictionary containing current forecast data
        """
        return await self.get_forecast(model_id, datetime_str=None)
    
    async def get_forecast_summary(self, model_id: str, datetime_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a summary of forecast conditions.
        
        Args:
            model_id: ID of the forecast model
            datetime_str: Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)
            
        Returns:
            Dictionary containing forecast summary
        """
        try:
            logger.info(f"Getting forecast summary for model {model_id}")
            
            # Get forecast data
            forecast_response = await self.get_forecast(model_id, datetime_str)
            
            if not forecast_response['success']:
                return forecast_response
            
            forecasts = forecast_response['data']['forecasts']
            
            if not forecasts:
                return {
                    'success': False,
                    'error': 'No forecast data available',
                    'message': f'No forecast data found for model {model_id}'
                }
            
            # Get the first forecast entry for summary
            forecast_data = forecasts[0]
            
            # Create summary
            summary = {
                'model_id': model_id,
                'forecast_datetime': datetime_str or 'current',
                'temperature': forecast_data.get('temperature'),
                'humidity': forecast_data.get('humidity'),
                'pressure': forecast_data.get('pressure'),
                'wind_speed': forecast_data.get('wind_speed'),
                'wind_direction': forecast_data.get('wind_direction'),
                'visibility': forecast_data.get('visibility'),
                'precipitation': forecast_data.get('precipitation'),
                'fog_probability': forecast_data.get('fog_probability'),
                'timestamp': forecast_data.get('timestamp')
            }
            
            return {
                'success': True,
                'data': summary,
                'message': f'Forecast summary retrieved for model {model_id}'
            }
            
        except Exception as e:
            logger.error(f"Error getting forecast summary: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve forecast summary'
            }
    
    async def compare_models(self, model_ids: List[str], datetime_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Compare forecasts from multiple models.
        
        Args:
            model_ids: List of model IDs to compare
            datetime_str: Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)
            
        Returns:
            Dictionary containing comparison data
        """
        try:
            logger.info(f"Comparing models: {model_ids}")
            
            comparison_data = {}
            
            for model_id in model_ids:
                forecast_response = await self.get_forecast(model_id, datetime_str)
                
                if forecast_response['success']:
                    comparison_data[model_id] = {
                        'success': True,
                        'data': forecast_response['data']['forecasts'][0] if forecast_response['data']['forecasts'] else None
                    }
                else:
                    comparison_data[model_id] = {
                        'success': False,
                        'error': forecast_response['error']
                    }
            
            return {
                'success': True,
                'data': {
                    'comparison_datetime': datetime_str or 'current',
                    'models': comparison_data,
                    'model_count': len(model_ids)
                },
                'message': f'Compared forecasts from {len(model_ids)} models'
            }
            
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to compare model forecasts'
            }
