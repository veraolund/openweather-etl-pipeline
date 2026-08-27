import logging
from extract import extract
from transform import transform
from load import load
from verify import verify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("data/open_weather_api.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Runs the full ETL pipeline, including verification.

    This function executes the sequential pipeline stages extract, transform, load and 
    verify. If a stage raises an exception, the error is propagated up. The start and 
    completion of the pipeline is logged into data/open_weather_api.log".
    """
    logger.info("Pipeline started")

    extract()
    transform()
    load()
    verify()

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    main()