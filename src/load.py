import os
import json
import psycopg
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def load():
    """
    Loads transformed weather data into PostgreSQL database.

    This function reads transformed weather data from a local JSON file, connects
    to a local PostgreSQL database, and runs an insertion query with values from 
    the JSON file.

    Envorinment Variables:
    - DB_NAME (str): Name of target database
    - DB_PASSWORD (str): Password for the postgres user

    Side effects:
    - Reads from data/transformed_data.json
    - Inserts a record into the database table weather_data
    - Logs messages to a configured logger

    Raises:
    - FileNotFoundError: If the input file is not found
    - json.JSONDecodeError: If the input file contains invalid JSON data
    - psycopg.OperationalError: If the database connection is unsuccessful
    - psycopg.Error: If a database error occurs other than a connection error
    - Exception: If an unexpected error occurs
    """
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    conn_string = (
        f"dbname={db_name} user={db_user} password={db_password} "
        f"host={db_host} port={db_port} sslmode=require"
    )

    try:
        with open("data/transformed_data.json", "r", encoding="utf-8") as file:
            weather = json.load(file)


        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # ON CONFLICT prevents insertion of duplicate rows with identical city and observation time
                insert_query = """
                    INSERT INTO weather_data(city, temperature, humidity, description, observed_at)
                    VALUES(%s, %s, %s, %s, %s)
                    ON CONFLICT (city, observed_at) DO NOTHING
                """

                cur.execute(
                    insert_query, 
                    (
                        weather["city"],
                        weather["temperature"],
                        weather["humidity"],
                        weather["description"],
                        weather["observed_at"]
                    )
                )
            conn.commit()

        logger.info(f"Weather data loaded successfully")

    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
        raise

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise

    except psycopg.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise

    except psycopg.Error as e:
        logger.error(f"Database error: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected loading error: {e}")
        raise