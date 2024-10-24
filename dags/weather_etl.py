from datetime import datetime, timedelta
import logging
from airflow.decorators import dag, task
from airflow.models import Variable
from tasks.extract import WeatherDataExtractor
from tasks.init_db import init_db
from tasks.transform import WeatherDataTransformer
from tasks.load import WeatherDataLoader
from tasks.utils import validate_cities
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False
}


@dag(
    dag_id='weather_etl',
    default_args=default_args,
    description='ETL pipeline for weather data',
    schedule_interval='*/10 * * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def weather_etl():
    init_database = init_db()

    @task
    def extract_weather_data() -> List[Dict]:
        logger.info('Starting weather data extraction')

        cities = Variable.get('CITIES', deserialize_json=True)
        validated_cites = validate_cities(cities)

        api_key = Variable.get('OPEN_WEATHER_API_KEY')
        extractor = WeatherDataExtractor(api_key)

        return extractor.get_weather_data(validated_cites)

    @task
    def transform_weather_data(weather_data: List[Dict]) -> List[Dict]:
        logger.info("Starting weather data transformation")

        transformer = WeatherDataTransformer()

        return transformer.transform_data(weather_data)

    @task
    def load_weather_data(transformed_data: List[Dict]):
        logger.info("Starting weather data loading")

        loader = WeatherDataLoader()
        loader.load_data(transformed_data)

    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_task= load_weather_data(transformed_data)

    init_database >> weather_data >> transformed_data >> load_task

dag_instance = weather_etl()
