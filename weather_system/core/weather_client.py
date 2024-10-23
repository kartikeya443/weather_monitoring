import aiohttp
import asyncio
from typing import Dict, List
from weather_system.config.settings import Settings
from weather_system.models.weather_data import WeatherData

class WeatherClient:
    def __init__(self, api_key: str = Settings.API_KEY):
        self.api_key = api_key
        self.base_url = Settings.BASE_URL

    async def get_weather_data(self, city_id: str, city_name: str) -> WeatherData:
        params = {
            'id': city_id,
            'appid': self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return WeatherData.from_api_response(data, city_name, city_id)
                else:
                    raise Exception(f"Failed to fetch weather data for {city_name}")

    async def get_weather_for_all_cities(self) -> List[WeatherData]:
        tasks = []
        for city in Settings.CITIES:
            tasks.append(self.get_weather_data(city['id'], city['name']))
        return await asyncio.gather(*tasks)