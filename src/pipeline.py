import logging
from extract import extract
from transform import transform
from load import load
from verify import verify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("data/open_weather_api.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Pipeline started")

    extract()
    transform()
    load()
    verify()

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    main()