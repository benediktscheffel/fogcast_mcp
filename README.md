# Fogcast MCP Server

A Python MCP (Model Context Protocol) server for accessing weather data in Konstanz, Germany. This server provides tools for retrieving current weather conditions and weather forecasts from the Fogcast data interface using the official MCP protocol.

## Features

- **Current Weather Data**: Access live weather measurements from DWD, OpenMeteo, and local weather stations
- **Weather Forecasts**: Retrieve forecasts from multiple weather models
- **Model Comparison**: Compare forecasts from different weather models
- **MCP Protocol**: Full MCP server implementation using official MCP libraries
- **Async Support**: Asynchronous operations for better performance

## Project Structure

```
fogcast_mcp/
├── main.py              # Main entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── env.example         # Environment configuration template
├── tests/              # Test suite
│   ├── __init__.py
│   └── test_app.py
└── src/                # Source code package
    └── fogcast_mcp/    # Main package
        ├── __init__.py
        ├── app.py      # MCP server application
        ├── config.py   # Configuration management
        ├── models/     # Data models and DTOs
        │   ├── __init__.py
        │   ├── weather_data.py
        │   └── api_response.py
        ├── integration/ # External API integration
        │   ├── __init__.py
        │   ├── http_client.py
        │   └── fogcast_client.py
        └── tools/      # MCP tool implementations
            ├── __init__.py
            ├── weather_tools.py
            └── forecast_tools.py
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fogcast_mcp
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The server uses environment variables for configuration. Create a `.env` file or set the following environment variables:

### Required Configuration

- `FOGCAST_BASE_URL`: Base URL of the Fogcast API server (default: `http://localhost:5000`)

### Optional Configuration

- `FOGCAST_TIMEOUT`: Request timeout in seconds (default: `30`)
- `FLASK_HOST`: Flask server host (default: `0.0.0.0`)
- `FLASK_PORT`: Flask server port (default: `5001`)
- `FLASK_DEBUG`: Enable Flask debug mode (default: `False`)
- `MCP_SERVER_NAME`: MCP server name (default: `fogcast-weather`)
- `MCP_SERVER_VERSION`: MCP server version (default: `1.0.0`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Example .env file

```env
FOGCAST_BASE_URL=http://your-fogcast-server:5000
FLASK_PORT=5001
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

## Usage

### Starting the Server

```bash
python main.py
```

The server will start in MCP stdio mode and communicate via stdin/stdout.

### Available Tools

The MCP server provides the following tools:

#### 1. Get Current Weather
- **Tool**: `get_current_weather`
- **Description**: Get current weather data for Konstanz
- **Parameters**: None

#### 2. Get Weather Summary
- **Tool**: `get_weather_summary`
- **Description**: Get a summary of current weather conditions
- **Parameters**: None

#### 3. Get Available Models
- **Tool**: `get_available_models`
- **Description**: Get list of available forecast models
- **Parameters**: None

#### 4. Get Forecast
- **Tool**: `get_forecast`
- **Description**: Get weather forecast for a specific model and datetime
- **Parameters**: 
  - `model_id` (required): ID of the forecast model
  - `datetime` (optional): Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ

#### 5. Get Current Forecast
- **Tool**: `get_current_forecast`
- **Description**: Get current forecast for a specific model
- **Parameters**: 
  - `model_id` (required): ID of the forecast model

#### 6. Get Forecast Summary
- **Tool**: `get_forecast_summary`
- **Description**: Get a summary of forecast conditions
- **Parameters**: 
  - `model_id` (required): ID of the forecast model
  - `datetime` (optional): Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ

#### 7. Compare Models
- **Tool**: `compare_models`
- **Description**: Compare forecasts from multiple models
- **Parameters**: 
  - `model_ids` (required): List of model IDs to compare
  - `datetime` (optional): Forecast datetime in format YYYY-MM-DDTHH:MM:SSZ

### Available Resources

The MCP server also provides the following resources:

- `fogcast://models` - List of available forecast models
- `fogcast://current-weather` - Current weather data for Konstanz
- `fogcast://weather-summary` - Summary of current weather conditions

## MCP Protocol

This server implements the Model Context Protocol (MCP) and communicates via stdin/stdout. It provides:

- **Tools**: Executable functions for weather data access
- **Resources**: Readable data sources for weather information
- **Async Operations**: All operations are asynchronous for better performance

## Data Models

### Weather Data
- `timestamp`: ISO format datetime
- `temperature`: Temperature in Celsius
- `humidity`: Humidity percentage
- `pressure`: Atmospheric pressure in hPa
- `wind_speed`: Wind speed in m/s
- `wind_direction`: Wind direction in degrees
- `visibility`: Visibility in meters
- `precipitation`: Precipitation in mm
- `fog_probability`: Fog probability (0-1)

### API Response
All API responses follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "error": null
}
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
flake8 .
```

### Type Checking

```bash
mypy .
```

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t fogcast-mcp .
docker run -e FOGCAST_BASE_URL=http://your-fogcast-server:5000 fogcast-mcp
```

## Error Handling

The server includes comprehensive error handling:

- **Connection Errors**: Handles network connectivity issues
- **Timeout Errors**: Manages request timeouts
- **HTTP Errors**: Processes HTTP status codes
- **Validation Errors**: Validates input parameters
- **Data Processing Errors**: Handles malformed data gracefully

## Logging

The server uses structured logging with configurable levels:

- `DEBUG`: Detailed debugging information
- `INFO`: General information about operations
- `WARNING`: Warning messages for non-critical issues
- `ERROR`: Error messages for failed operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the development team.
