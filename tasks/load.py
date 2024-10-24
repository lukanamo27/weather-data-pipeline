import logging
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import List, Dict


class WeatherDataLoader:
    def __init__(self, conn_id: str = 'postgres_default'):
        self.conn_id = conn_id
        self.logger = logging.getLogger(__name__)

    def load_data(self, data: List[Dict]):
        if not data:
            self.logger.warning('No data to load')
            return

        try:
            df = pd.DataFrame(data)
            pg_hook = PostgresHook(postgres_conn_id=self.conn_id)
            engine = pg_hook.get_sqlalchemy_engine()

            with engine.begin() as connection:
                df.to_sql(
                    'weather_history',
                    connection,
                    if_exists='append',
                    index=False
                )
                self.logger.info(
                    f'Successfully loaded {len(data)} records to history'
                )

                for record in data:
                    upsert_query ="""
                    INSERT INTO current_weather 
                        (city, country, temperature, humidity, pressure, 
                         weather_description, wind_speed, timestamp, updated_at)
                    VALUES 
                        (%(city)s, %(country)s, %(temperature)s, %(humidity)s, 
                         %(pressure)s, %(weather_description)s, %(wind_speed)s, 
                         %(timestamp)s, CURRENT_TIMESTAMP)
                    ON CONFLICT (city) DO UPDATE SET
                        country = EXCLUDED.country,
                        temperature = EXCLUDED.temperature,
                        humidity = EXCLUDED.humidity,
                        pressure = EXCLUDED.pressure,
                        weather_description = EXCLUDED.weather_description,
                        wind_speed = EXCLUDED.wind_speed,
                        timestamp = EXCLUDED.timestamp,
                        updated_at = CURRENT_TIMESTAMP;
                    """
                    connection.execute(
                        upsert_query,
                        {
                            'city': record['city'],
                            'country': record['country'],
                            'temperature': record['temperature'],
                            'humidity': record['humidity'],
                            'pressure': record['pressure'],
                            'weather_description': record['weather_description'],
                            'wind_speed': record['wind_speed'],
                            'timestamp': record['timestamp']
                        }
                    )
                    self.logger.info('Successfully updated current weather records')
        except Exception as e:
            self.logger.error(f'Error loading data to PostgreSQL: {str(e)}')
            raise
