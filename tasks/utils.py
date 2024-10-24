import logging
from typing import List

logger = logging.getLogger(__name__)


def validate_cities(cities: List[str]) -> List[str]:
    valid_cities = []

    for city in cities:
        if isinstance(city, str) and city.strip():
            valid_cities.append(city.strip())
        else:
            logger.warning(f'Invalid city name: {city}')

    return valid_cities
