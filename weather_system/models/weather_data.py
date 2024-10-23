from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class WeatherData:
    city_name: str
    city_id: str
    temperature: float
    feels_like: float
    weather_condition: str
    timestamp: datetime
    
    @classmethod
    def from_api_response(cls, response: dict, city_name: str, city_id: str):
        return cls(
            city_name=city_name,
            city_id=city_id,
            temperature=response['main']['temp'],
            feels_like=response['main']['feels_like'],
            weather_condition=response['weather'][0]['main'],
            timestamp=datetime.fromtimestamp(response['dt'])
        )