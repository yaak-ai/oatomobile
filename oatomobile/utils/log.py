import sys
import json
import logging

import numpy as np

SERVICE_LOGGING_FORMAT = (
    "[{filename:s}][{funcName:s}:{lineno:d}]" + "[{levelname:s}] {message:s}"
)
SERVICE_LOGGING_STREAM = sys.stdout


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int):
            return int(obj)
        elif isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JSONEncoder, self).default(obj)


def get_logger(logger_name, log_level="info"):

    SERVICE_LOGGING_LEVEL = getattr(logging, log_level.upper(), None)

    logger = logging.getLogger(logger_name)
    logger.setLevel(SERVICE_LOGGING_LEVEL)
    ch = logging.StreamHandler(SERVICE_LOGGING_STREAM)
    formatter = logging.Formatter(SERVICE_LOGGING_FORMAT, style="{")
    ch.setFormatter(formatter)
    ch.setLevel(SERVICE_LOGGING_LEVEL)
    logger.addHandler(ch)
    logger.propagate = False

    return logger
