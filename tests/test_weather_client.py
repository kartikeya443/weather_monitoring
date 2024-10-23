import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime
from weather_system.core.weather_client import WeatherClient
from weather_system.models.weather_data import WeatherData

@pytest.mark.asyncio
async def test_get_weather_data():
    mock_response = {
        'main': {'temp': 300.15, 'feels_like': 305.15},
        'weather': [{'main': 'Clear'}],
        'dt': int(datetime.now().timestamp())
    }
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = lambda: mock_response
        
        client = WeatherClient(api_key="test_key")
        weather_data = await client.get_weather_data("1273294", "Delhi")
        
        assert isinstance(weather_data, WeatherData)
        assert weather_data.city_name == "Delhi"
        assert weather_data.temperature == 300.15
        assert weather_data.weather_condition == "Clear"