import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def transform():
    """
    Transforms raw JSON payload into a condensed, flat format. 

    This function reads the raw payload from a local file, extracts neccessary 
    metrics (city, temperature, humidity, time of observation), and writes the 
    transformed data to another local file.

    Side effects:
    - Reads from data/raw_weather.json
    - Writes (or overwrites) flat JSON key-value pairs to data/transformed_data.json
    - Logs messages to a configured logger

    Output Schema:
    - city (str): Name of city
    - temperature (float): Current temperature
    - humidity (float): Current humidity
    - description (str): Weather description
    - observed_at (str): ISO 8601 UTC timestamp for the observation

    Raises:
    - FileNotFoundError: If the file is not found
    - json.JSONDecodeError: If the input file contains invalid JSON data
    - KeyError: If expected keys are missing from input file
    - Exception: If an unexpected error occurs
    """
    try:
        with open("data/raw_weather.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        transformed_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"], 
            "humidity": data["main"]["humidity"], 
            "description": data["weather"][0]["description"],
            "observed_at": datetime.fromtimestamp(data["dt"], tz=timezone.utc).isoformat()
        }

        with open("data/transformed_data.json", "w", encoding="utf-8") as file:
            json.dump(transformed_data, file, indent=4)

        logger.info("Weather data transformed successfully")

    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
        raise

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise

    except KeyError as e:
        logger.error(f"Expected field missing from API data: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected transformation error: {e}")
        raise