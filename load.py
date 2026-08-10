import os
import json
import psycopg
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def load():
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    conn_string = (
        f"dbname=LearnAPI user=postgres password={db_password} "
        f"host=localhost port=5432"
    )

    try:
        with open("transformed_data.json", "r", encoding="utf-8") as file:
            weather = json.load(file)


        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                insert_query = """
                    INSERT INTO weather_data(
                        city,
                        temperature,
                        humidity,
                        description
                    )
                    VALUES(%s, %s, %s, %s)
                """

                cur.execute(
                    insert_query, 
                    (
                        weather["city"],
                        weather["temperature"],
                        weather["humidity"],
                        weather["description"]
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