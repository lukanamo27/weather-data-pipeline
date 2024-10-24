# Weather Data Pipeline

An Airflow ETL pipeline that collects weather data from OpenWeather API, processes it, and stores both current weather and historical weather data in PostgreSQL database.

## Features

- Collects weather data for configured cities every 10 minutes
- Stores historical weather data
- Maintains current weather information
- Uses Docker for containerization
- Implements proper error handling and logging

## Prerequisites

- Docker and Docker Compose
- OpenWeather API key
- Python 3.8+

## Project Structure

```
weather-data-pipeline/
├── dags/
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── extract.py
│   │   ├── transform.py
│   │   ├── load.py
│   │   ├── init_db.py
│   │   └── utils.py
│   └── weather_etl.py
├── logs/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-data-pipeline.git
cd weather-data-pipeline
```

2. Create a `.env` file with your configuration:
```bash
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_passowrd
POSTGRES_DB=your_db
OPEN_WEATHER_API_KEY=your_api_key
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access Airflow web interface at `http://localhost:8080`

5. Add the following variables in Airflow:
   - `OPEN_WEATHER_API_KEY`: Your OpenWeather API key
   - `CITIES`: List of cities to monitor (as JSON array)

## Database Schema

### Current Weather Table
- Stores the latest weather data for each city
- Uses city name as a unique key for upserts

### Weather History Table
- Stores all historical weather data
- Includes timestamp for tracking weather changes
- Indexed for efficient querying
