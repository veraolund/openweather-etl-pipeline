import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def transform():
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