import pytest
from datetime import datetime
from weather_system.core.data_processor import DataProcessor, WeatherAggregator
from weather_system.models.weather_data import WeatherData

def test_temperature_conversion():
    processor = DataProcessor()
    
    test_data = WeatherData(
        city_name="Delhi",
        city_id="1273294",
        temperature=300.15,  # Kelvin
        feels_like=305.15,   # Kelvin
        weather_condition="Clear",
        timestamp=datetime.now()
    )
    
    processed_data = processor.process_weather_data(test_data)
    assert round(processed_data.temperature, 2) == 27.0  # 300.15K - 273.15 = 27°C
    assert round(processed_data.feels_like, 2) == 32.0   # 305.15K - 273.15 = 32°C

def test_weather_aggregator():
    aggregator = WeatherAggregator()
    
    # Create test data for multiple readings
    test_data = [
        WeatherData("Delhi", "1273294", 25.0, 27.0, "Clear", datetime.now()),
        WeatherData("Delhi", "1273294", 27.0, 29.0, "Clear", datetime.now()),
        WeatherData("Delhi", "1273294", 26.0, 28.0, "Clouds", datetime.now())
    ]
    
    for data in test_data:
        aggregator.add_reading(data)
    
    summary = aggregator.get_daily_summary(datetime.now().date())
    
    assert summary is not None
    assert summary['city'] == "Delhi"
    assert summary['avg_temperature'] == 26.0
    assert summary['max_temperature'] == 27.0
    assert summary['min_temperature'] == 25.0
    assert summary['dominant_condition'] == "Clear"