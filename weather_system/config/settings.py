import os
from typing import List, Dict

class Settings:
    # OpenWeatherMap API settings
    API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "ddd280e6940085c4aee0c2574fc5c151")
    BASE_URL: str = "http://api.openweathermap.org/data/2.5/weather"
    
    # Cities to monitor
    CITIES: List[Dict[str, str]] = [
        {"name": "Delhi", "id": "1273294"},
        {"name": "Mumbai", "id": "1275339"},
        {"name": "Chennai", "id": "1264527"},
        {"name": "Bangalore", "id": "1277333"},
        {"name": "Kolkata", "id": "1275004"},
        {"name": "Hyderabad", "id": "1269843"}
    ]
    
    # Data collection settings
    POLLING_INTERVAL: int = 300  # 5 minutes in seconds
    
    # Temperature thresholds
    DEFAULT_HIGH_TEMP_THRESHOLD: float = 35.0
    DEFAULT_CONSECUTIVE_READINGS: int = 2
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///weather_data.db")