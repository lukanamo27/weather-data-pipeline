from datetime import datetime, timezone, timedelta
import logging
from typing import List, Dict


class WeatherDataTransformer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def transform_data(self, raw_data: List[Dict]) -> List[Dict]:
        transformed_data = []
        tbilisi_tz = timezone(timedelta(hours=4))

        for data in raw_data:
            try:
                transformed_data.append({
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'weather_description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed'],
                    'timestamp': datetime.fromtimestamp(
                        data['dt'], tz=tbilisi_tz
                    ).isoformat()
                })
                self.logger.info('Weather data transformed successfully')
            except KeyError as e:
                self.logger.error(f'Error transforming data. Missing key {str(e)}')
                continue

        return transformed_data
