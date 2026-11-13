
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "game.log"


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger
