import logging


_logger = None


def get_logger() -> logging.Logger:
    global _logger
    if _logger is None:
        raise NotImplementedError("Logger not set")
    return _logger


def set_logger(logger: logging.Logger):
    global _logger
    _logger = logger
    pass
