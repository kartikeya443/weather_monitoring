from typing import Dict, List
from datetime import datetime, timedelta
from weather_system.models.weather_data import WeatherData
from weather_system.config.settings import Settings

class ThresholdAlert:
    def __init__(self, city: str, condition: str, value: float, timestamp: datetime):
        self.city = city
        self.condition = condition
        self.value = value
        self.timestamp = timestamp

class ThresholdManager:
    def __init__(self):
        self.temperature_threshold = Settings.DEFAULT_HIGH_TEMP_THRESHOLD
        self.consecutive_readings = Settings.DEFAULT_CONSECUTIVE_READINGS
        self.recent_readings: Dict[str, List[WeatherData]] = {}
        self.active_alerts: List[ThresholdAlert] = []

    def check_thresholds(self, weather_data: WeatherData) -> List[ThresholdAlert]:
        """Check if weather data exceeds defined thresholds"""
        new_alerts = []
        
        # Update recent readings
        if weather_data.city_id not in self.recent_readings:
            self.recent_readings[weather_data.city_id] = []
        
        readings = self.recent_readings[weather_data.city_id]
        readings.append(weather_data)
        
        # Keep only recent readings within consecutive window
        cutoff_time = datetime.now() - timedelta(minutes=30)
        readings = [r for r in readings if r.timestamp > cutoff_time]
        self.recent_readings[weather_data.city_id] = readings
        
        # Check temperature threshold
        if len(readings) >= self.consecutive_readings:
            recent_temps = [r.temperature for r in readings[-self.consecutive_readings:]]
            if all(temp > self.temperature_threshold for temp in recent_temps):
                alert = ThresholdAlert(
                    city=weather_data.city_name,
                    condition="High Temperature",
                    value=weather_data.temperature,
                    timestamp=weather_data.timestamp
                )
                new_alerts.append(alert)
                self.active_alerts.append(alert)
        
        return new_alerts
