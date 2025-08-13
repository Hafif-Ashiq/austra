import os, sys, logging, logging.handlers
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

def setup_logger(name: str, log_to_stdout=True, level=logging.DEBUG) -> logging.Logger:
    load_dotenv()

    log_directory = os.getenv("PATH_LOGS", os.path.expanduser("~"))
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, f"{name}.log")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Handler fichier avec rotation
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Handler stdout si demandé
        if log_to_stdout:
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        logger.propagate = False

    return logger
