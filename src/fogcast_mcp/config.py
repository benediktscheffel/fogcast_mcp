"""
Configuration management for the Fogcast MCP Server.
Handles environment variables and provides centralized configuration.
"""

import os
from typing import Optional


class Config:
    """Configuration class that loads settings from environment variables."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        # Fogcast API Configuration
        self.fogcast_base_url = os.getenv('FOGCAST_BASE_URL', 'http://localhost:5000')
        self.fogcast_timeout = int(os.getenv('FOGCAST_TIMEOUT', '30'))
        
        # Flask Configuration
        self.flask_host = os.getenv('FLASK_HOST', '0.0.0.0')
        self.flask_port = int(os.getenv('FLASK_PORT', '5001'))
        self.flask_debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        # MCP Configuration
        self.mcp_server_name = os.getenv('MCP_SERVER_NAME', 'fogcast-weather')
        self.mcp_server_version = os.getenv('MCP_SERVER_VERSION', '1.0.0')
        
        # Logging Configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
    def validate(self) -> None:
        """Validate that all required configuration is present."""
        required_configs = [
            ('fogcast_base_url', self.fogcast_base_url),
        ]
        
        missing_configs = []
        for name, value in required_configs:
            if not value:
                missing_configs.append(name)
        
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
    
    def __repr__(self) -> str:
        """String representation of configuration (excluding sensitive data)."""
        return (
            f"Config("
            f"fogcast_base_url='{self.fogcast_base_url}', "
            f"flask_host='{self.flask_host}', "
            f"flask_port={self.flask_port}, "
            f"mcp_server_name='{self.mcp_server_name}'"
            f")"
        )


# Global configuration instance
config = Config()
