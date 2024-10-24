import requests
import logging
from typing import List, Dict


class WeatherDataExtractor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather'
        self.logger = logging.getLogger(__name__)

    def get_weather_data(self, cities: List[str]) -> List[Dict]:
        weather_data = []
        for city in cities:
            try:
                params = {
                    'q': city,
                    'appid': self.api_key,
                    'units': 'metric'
                }
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                weather_data.append(response.json())
                self.logger.info('Weather data extracted successfully')
            except requests.RequestException as e:
                self.logger.error(f'Error fetching data for {city}: {str(e)}')
                continue

        return weather_data
