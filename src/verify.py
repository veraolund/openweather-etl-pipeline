import os
import psycopg
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def verify():
    """
    Verifies expected data exists in PostgreSQL table weather_data.

    This function connects to a local PostgreSQL database (hosted on Neon), verifies 
    that the weather_data table is not empty, selects the latest inserted record and 
    verifies that vital values exist and are within a valid range. 
    
    Environment Variables:
    - DB_HOST (str): Hostname of the database server
    - DB_PORT (str): Port number of the database server
    - DB_NAME (str): Name of target database
    - DB_USER (str): Username for database authentication
    - DB_PASSWORD (str): Password for database authentication

    Side effects:
    - Queries the database table weather_data
    - Logs messages to a configured logger

    Raises:
    - psycopg.OperationalError: If the database connection is unsuccessful
    - psycopg.Error: If a database error occurs other than a connection error
    - ValueError: If city or temperature is NULL, or if humidity is NULL or out of range
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
                    SELECT city, temperature, humidity, description, observed_at
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