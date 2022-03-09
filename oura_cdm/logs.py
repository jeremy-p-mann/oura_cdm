import logging
from logging import Logger
from typing import Dict

LOGGERS: Dict[str, Logger] = {}


def get_logger(name: str) -> Logger:
    if name in LOGGERS.keys():
        return LOGGERS[name]
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    LOGGERS[name] = logger
    logger.propagate = False
    return logger


def log_warning(message, name):
    get_logger(name).log(logging.WARNING, message)


def log_info(message, name):
    get_logger(name).log(logging.INFO, message)
