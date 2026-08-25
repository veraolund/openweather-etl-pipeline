import os
import json
import requests
import logging
from dotenv import load_dotenv
 
logger = logging.getLogger(__name__)

def extract():
    load_dotenv()
    latitude = os.getenv("CITY_LAT")
    longitude = os.getenv("CITY_LON")
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric"
    }

    try: 
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        with open("data/raw_weather.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        logger.info(f"Weather data successfully extracted and saved")

    except requests.exceptions.HTTPError as e:
        logger.error(f"API answered with status code: {e.response.status_code}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"Could not reach API: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected extraction error: {e}")
        raise