"""
HTTP client for making API requests using httpx.
"""

import httpx
from typing import Dict, Any, Optional
import logging
from config import config


logger = logging.getLogger(__name__)


class HTTPClient:
    """HTTP client for making API requests with error handling."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize HTTP client.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint (without leading slash)
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            httpx.RequestError: If request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"Making GET request to {url} with params: {params}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            # Try to parse JSON, fallback to text if not JSON
            try:
                return response.json()
            except ValueError:
                return {'data': response.text}
                
        except httpx.TimeoutException:
            logger.error(f"Request timeout for {url}")
            raise httpx.RequestError(f"Request timeout for {url}")
        except httpx.ConnectError:
            logger.error(f"Connection error for {url}")
            raise httpx.RequestError(f"Connection error for {url}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise httpx.RequestError(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            raise httpx.RequestError(f"Unexpected error: {e}")
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint (without leading slash)
            data: Request body data
            
        Returns:
            Response data as dictionary
            
        Raises:
            httpx.RequestError: If request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            logger.debug(f"Making POST request to {url} with data: {data}")
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            
            # Try to parse JSON, fallback to text if not JSON
            try:
                return response.json()
            except ValueError:
                return {'data': response.text}
                
        except httpx.TimeoutException:
            logger.error(f"Request timeout for {url}")
            raise httpx.RequestError(f"Request timeout for {url}")
        except httpx.ConnectError:
            logger.error(f"Connection error for {url}")
            raise httpx.RequestError(f"Connection error for {url}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise httpx.RequestError(f"HTTP error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}")
            raise httpx.RequestError(f"Unexpected error: {e}")
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
