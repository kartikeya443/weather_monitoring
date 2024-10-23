from typing import List, Dict
from collections import Counter
from datetime import datetime, timedelta
from weather_system.models.weather_data import WeatherData
from weather_system.utils.temperature_converter import TemperatureConverter

class DataProcessor:
    def __init__(self):
        self.temp_converter = TemperatureConverter()

    def process_weather_data(self, weather_data: WeatherData) -> WeatherData:
        """Process raw weather data by converting temperatures"""
        weather_data.temperature = self.temp_converter.kelvin_to_celsius(weather_data.temperature)
        weather_data.feels_like = self.temp_converter.kelvin_to_celsius(weather_data.feels_like)
        return weather_data

class WeatherAggregator:
    def __init__(self):
        self.daily_readings: Dict[str, List[WeatherData]] = {}

    def add_reading(self, weather_data: WeatherData):
        """Add a new weather reading to the daily aggregation"""
        date_key = weather_data.timestamp.date().isoformat()
        if date_key not in self.daily_readings:
            self.daily_readings[date_key] = []
        self.daily_readings[date_key].append(weather_data)

    def get_daily_summary(self, date: datetime.date) -> Dict:
        """Calculate daily summary for a specific date"""
        date_key = date.isoformat()
        if date_key not in self.daily_readings:
            return None

        readings = self.daily_readings[date_key]
        temperatures = [r.temperature for r in readings]
        conditions = [r.weather_condition for r in readings]

        # Find dominant weather condition using Counter
        condition_counts = Counter(conditions)
        dominant_condition = condition_counts.most_common(1)[0][0]
        
        return {
            'date': date,
            'city': readings[0].city_name,
            'avg_temperature': sum(temperatures) / len(temperatures),
            'max_temperature': max(temperatures),
            'min_temperature': min(temperatures),
            'dominant_condition': dominant_condition,
            'condition_distribution': dict(condition_counts),
            'reading_count': len(readings)
        }