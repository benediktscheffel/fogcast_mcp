#!/usr/bin/env python3
"""
Fogcast MCP Server - Provides weather data for Konstanz
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional
import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
)
from pydantic import BaseModel

from .config import config
from .integration.fogcast_client import FogcastClient
from .tools.weather_tools import WeatherTools
from .tools.forecast_tools import ForecastTools

# Logging Setup
logging.basicConfig(level=getattr(logging, config.log_level.upper()))
logger = logging.getLogger(__name__)

# Server initialisieren
app = Server(config.mcp_server_name)

# Initialize clients and tools
fogcast_client = FogcastClient()
weather_tools = WeatherTools(fogcast_client)
forecast_tools = ForecastTools(fogcast_client)


# Pydantic Models für strukturierte Daten
class WeatherRequest(BaseModel):
    model_id: Optional[str] = None
    datetime: Optional[str] = None


class ModelComparisonRequest(BaseModel):
    model_ids: List[str]
    datetime: Optional[str] = None


@app.list_resources()
async def list_resources() -> List[Resource]:
    """Liste verfügbare Wetter-Ressourcen"""
    return [
        Resource(
            uri="fogcast://models",
            name="Available Models",
            description="List of all available forecast models",
            mimeType="application/json"
        ),
        Resource(
            uri="fogcast://current-weather",
            name="Current Weather",
            description="Current weather data for Konstanz",
            mimeType="application/json"
        ),
        Resource(
            uri="fogcast://weather-summary",
            name="Weather Summary",
            description="Summary of current weather conditions",
            mimeType="application/json"
        )
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Lese spezifische Wetter-Ressource"""
    try:
        if uri == "fogcast://models":
            response = await forecast_tools.get_available_models()
            return json.dumps(response, indent=2)
        
        elif uri == "fogcast://current-weather":
            response = await weather_tools.get_current_weather()
            return json.dumps(response, indent=2)
        
        elif uri == "fogcast://weather-summary":
            response = await weather_tools.get_weather_summary()
            return json.dumps(response, indent=2)
        
        else:
            return json.dumps({"error": "Resource not found"})
    
    except Exception as e:
        logger.error(f"Error reading resource {uri}: {e}")
        return json.dumps({"error": f"Failed to read resource: {str(e)}"})


@app.list_tools()
async def list_tools() -> List[Tool]:
    """Liste verfügbare Weather Tools"""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather data for Konstanz",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_weather_summary",
            description="Get a summary of current weather conditions",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_available_models",
            description="Get list of available forecast models",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_forecast",
            description="Get weather forecast for a specific model and datetime",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "ID of the forecast model"
                    },
                    "datetime": {
                        "type": "string",
                        "description": "Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)"
                    }
                },
                "required": ["model_id"]
            }
        ),
        Tool(
            name="get_current_forecast",
            description="Get current forecast for a specific model",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "ID of the forecast model"
                    }
                },
                "required": ["model_id"]
            }
        ),
        Tool(
            name="get_forecast_summary",
            description="Get a summary of forecast conditions",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_id": {
                        "type": "string",
                        "description": "ID of the forecast model"
                    },
                    "datetime": {
                        "type": "string",
                        "description": "Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)"
                    }
                },
                "required": ["model_id"]
            }
        ),
        Tool(
            name="compare_models",
            description="Compare forecasts from multiple models",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of model IDs to compare"
                    },
                    "datetime": {
                        "type": "string",
                        "description": "Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ (optional)"
                    }
                },
                "required": ["model_ids"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Führt Weather Tool-Aufrufe aus"""
    
    try:
        if name == "get_current_weather":
            result = await weather_tools.get_current_weather()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_weather_summary":
            result = await weather_tools.get_weather_summary()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_available_models":
            result = await forecast_tools.get_available_models()
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_forecast":
            model_id = arguments.get("model_id")
            if not model_id:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "model_id parameter is required"})
                )]
            
            datetime_str = arguments.get("datetime")
            result = await forecast_tools.get_forecast(model_id, datetime_str)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_current_forecast":
            model_id = arguments.get("model_id")
            if not model_id:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "model_id parameter is required"})
                )]
            
            result = await forecast_tools.get_current_forecast(model_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_forecast_summary":
            model_id = arguments.get("model_id")
            if not model_id:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "model_id parameter is required"})
                )]
            
            datetime_str = arguments.get("datetime")
            result = await forecast_tools.get_forecast_summary(model_id, datetime_str)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "compare_models":
            model_ids = arguments.get("model_ids")
            if not model_ids or not isinstance(model_ids, list):
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": "model_ids parameter is required and must be a list"})
                )]
            
            datetime_str = arguments.get("datetime")
            result = await forecast_tools.compare_models(model_ids, datetime_str)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"})
            )]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "message": f"Failed to execute tool {name}"
            })
        )]


async def main():
    """Hauptfunktion - startet den MCP Server"""
    try:
        # Validate configuration
        config.validate()
        
        logger.info(f"🌤️ Starting {config.mcp_server_name} v{config.mcp_server_version}")
        logger.info(f"📡 Fogcast API URL: {config.fogcast_base_url}")
        logger.info("📡 MCP stdio mode")
        
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream, 
                app.create_initialization_options()
            )
    
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    finally:
        # Clean up resources
        await fogcast_client.close()


if __name__ == "__main__":
    asyncio.run(main())