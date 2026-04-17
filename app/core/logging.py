import logging, sys
from app.config import get_settings

setting = get_settings()

LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
DATA_FORMAT = '%d-%m-%Y %H:%M:%S'


def setup_logging() -> None:
    level = logging.DEBUG if setting.app_debug else logging.INFO

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATA_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log', encoding='utf-8')
        ]
    )

    # silent
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)