import os
import psycopg
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def verify():
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    conn_string = (
        f"dbname={db_name} user=postgres password={db_password} "
        f"host=localhost port=5432"
    )

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*)
                    FROM weather_data;
                """)

                row_count = cur.fetchone()[0]

                if row_count == 0:
                    raise ValueError("Verification failed:  weather_data is empty")

                cur.execute("""
                    SELECT city, temperature, humidity, description
                    FROM weather_data
                    ORDER BY loaded_at DESC
                    LIMIT 1
                """)

                latest = cur.fetchone()

                if latest[0] is None:
                    raise ValueError("Verification failed: city is NULL.")

                if latest[1] is None:
                    raise ValueError("Verification failed: temperature is NULL.")
                
                if latest[2] is None or not 0 <= latest[2] <= 100:
                    raise ValueError("Verification failed: humidity is NULL or invalid.")
                

        logger.info(f"Verification completed successfully. Latest record for {latest[0]} is valid")  
        
    except psycopg.OperationalError as e:
        logger.error(f"Databse connection failed: {e}")
        raise

    except psycopg.Error as e:
        logger.error(f"Database error: {e}")
        raise

    except ValueError as e:
        logger.error(str(e))
        raise

    except Exception as e:
        logger.error(f"Unexpected verification error: {e}")
        raise