import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    logger.info("Initialization complete")

if __name__ == "__main__":
    logger.info("Starting initialization...")
    init()
