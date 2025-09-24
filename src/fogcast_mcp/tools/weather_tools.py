"""
MCP tools for current weather data access.
"""

from typing import Dict, Any, List
import logging

from ..integration.fogcast_client import FogcastClient
from ..models.api_response import APIResponse


logger = logging.getLogger(__name__)


class WeatherTools:
    """MCP tools for accessing current weather data."""
    
    def __init__(self, fogcast_client: FogcastClient):
        """
        Initialize weather tools.
        
        Args:
            fogcast_client: Fogcast API client instance
        """
        self.fogcast_client = fogcast_client
    
    async def get_current_weather(self) -> Dict[str, Any]:
        """
        Get current weather data for Konstanz.
        
        Returns:
            Dictionary containing current weather information
        """
        try:
            logger.info("Getting current weather data")
            
            # Fetch live data from Fogcast API
            response = await self.fogcast_client.get_live_data()
            
            if not response.success:
                return {
                    'success': False,
                    'error': response.error,
                    'message': response.message
                }
            
            # Format the response for MCP
            weather_data = response.data
            
            return {
                'success': True,
                'data': {
                    'location': 'Konstanz, Germany',
                    'current_conditions': weather_data,
                    'last_updated': weather_data[0].get('timestamp') if weather_data else None
                },
                'message': f"Retrieved current weather data with {len(weather_data)} data points"
            }
            
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve current weather data'
            }
    
    async def get_weather_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current weather conditions.
        
        Returns:
            Dictionary containing weather summary
        """
        try:
            logger.info("Getting weather summary")
            
            # Get current weather data
            weather_response = await self.get_current_weather()
            
            if not weather_response['success']:
                return weather_response
            
            current_data = weather_response['data']['current_conditions']
            
            if not current_data:
                return {
                    'success': False,
                    'error': 'No weather data available',
                    'message': 'No current weather data found'
                }
            
            # Extract the most recent data point
            latest_data = current_data[0] if current_data else {}
            
            # Create summary
            summary = {
                'location': 'Konstanz, Germany',
                'temperature': latest_data.get('temperature'),
                'humidity': latest_data.get('humidity'),
                'pressure': latest_data.get('pressure'),
                'wind_speed': latest_data.get('wind_speed'),
                'wind_direction': latest_data.get('wind_direction'),
                'visibility': latest_data.get('visibility'),
                'precipitation': latest_data.get('precipitation'),
                'water_level': latest_data.get('water_level'),
                'source': latest_data.get('source'),
                'last_updated': latest_data.get('timestamp')
            }
            
            return {
                'success': True,
                'data': summary,
                'message': 'Weather summary retrieved successfully'
            }
            
        except Exception as e:
            logger.error(f"Error getting weather summary: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to retrieve weather summary'
            }
