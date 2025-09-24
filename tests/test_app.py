"""
Tests for the main Flask application.
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fogcast_mcp.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check returns correct status."""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
        assert 'version' in data


class TestToolsEndpoint:
    """Test the tools listing endpoint."""
    
    def test_list_tools(self, client):
        """Test tools listing returns all available tools."""
        response = client.get('/tools')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'tools' in data
        assert 'count' in data
        assert data['count'] > 0
        
        # Check that expected tools are present
        tool_names = [tool['name'] for tool in data['tools']]
        expected_tools = [
            'get_current_weather',
            'get_weather_summary',
            'get_available_models',
            'get_forecast',
            'get_current_forecast',
            'get_forecast_summary',
            'compare_models'
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names


class TestToolExecution:
    """Test tool execution endpoints."""
    
    @patch('app.weather_tools')
    def test_get_current_weather(self, mock_weather_tools, client):
        """Test get_current_weather tool execution."""
        mock_weather_tools.get_current_weather.return_value = {
            'success': True,
            'data': {'temperature': 20.5},
            'message': 'Success'
        }
        
        response = client.post('/tools/get_current_weather',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    @patch('app.forecast_tools')
    def test_get_forecast_missing_model_id(self, mock_forecast_tools, client):
        """Test get_forecast tool with missing model_id parameter."""
        response = client.post('/tools/get_forecast',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'model_id parameter is required' in data['error']
    
    @patch('app.forecast_tools')
    def test_get_forecast_with_model_id(self, mock_forecast_tools, client):
        """Test get_forecast tool with valid model_id."""
        mock_forecast_tools.get_forecast.return_value = {
            'success': True,
            'data': {'forecasts': []},
            'message': 'Success'
        }
        
        response = client.post('/tools/get_forecast',
                             data=json.dumps({'model_id': 'test_model'}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_unknown_tool(self, client):
        """Test execution of unknown tool."""
        response = client.post('/tools/unknown_tool',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Unknown tool' in data['error']


class TestMCPInfo:
    """Test MCP server information endpoint."""
    
    def test_mcp_info(self, client):
        """Test MCP info endpoint returns correct information."""
        response = client.get('/mcp/info')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'name' in data
        assert 'version' in data
        assert 'description' in data
        assert 'capabilities' in data


class TestErrorHandling:
    """Test error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Endpoint not found' in data['error']
