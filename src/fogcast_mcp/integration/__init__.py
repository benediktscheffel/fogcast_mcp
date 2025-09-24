"""
Integration layer for external API communication.
"""

from .fogcast_client import FogcastClient
from .http_client import HTTPClient

__all__ = ['FogcastClient', 'HTTPClient']
