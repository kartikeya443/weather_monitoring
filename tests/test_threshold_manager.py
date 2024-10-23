import pytest
from weather_system.alerts.threshold_manager import ThresholdManager
from datetime import datetime
from weather_system.models.weather_data import WeatherData

def test_threshold_detection():
    manager = ThresholdManager()
    manager.temperature_threshold = 35.0
    manager.consecutive_readings = 2
    
    # Test data with temperatures above threshold
    test_data = [
        WeatherData("Delhi", "1273294", 36.0, 38.0, "Clear", datetime.now()),
        WeatherData("Delhi", "1273294", 37.0, 39.0, "Clear", datetime.now())
    ]
    
    # First reading should not trigger alert
    alerts = manager.check_thresholds(test_data[0])
    assert len(alerts) == 0
    
    # Second reading should trigger alert
    alerts = manager.check_thresholds(test_data[1])
    assert len(alerts) == 1
    assert alerts[0].condition == "High Temperature"
    assert alerts[0].city == "Delhi"