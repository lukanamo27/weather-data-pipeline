from airflow.decorators import task
import logging
from airflow.providers.postgres.hooks.postgres import PostgresHook


@task
def init_db():
    logger = logging.getLogger(__name__)
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')

    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS current_weather
    (
        id                  SERIAL PRIMARY KEY,
        city                VARCHAR(100) UNIQUE,
        country             VARCHAR(2),
        temperature         FLOAT,
        humidity            INTEGER,
        pressure            INTEGER,
        weather_description TEXT,
        wind_speed          FLOAT,
        timestamp           TIMESTAMP,
        updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS weather_history
    (
        id                  SERIAL PRIMARY KEY,
        city                VARCHAR(100),
        country             VARCHAR(2),
        temperature         FLOAT,
        humidity            INTEGER,
        pressure            INTEGER,
        weather_description TEXT,
        wind_speed          FLOAT,
        timestamp           TIMESTAMP,
        created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_weather_history_city_timestamp
        ON weather_history (city, timestamp);
    """

    try:
        conn = pg_hook.get_conn()
        cur = conn.cursor()
        cur.execute(create_tables_sql)
        conn.commit()
        logger.info("Successfully created/verified database tables")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()
