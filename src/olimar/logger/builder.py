import enum
import logging
import os
from logging.handlers import RotatingFileHandler


class LoggerBuilder:
    FORMAT = "[%(asctime)s][%(threadName)s][%(name)s.%(funcName)s:%(lineno)s][%(levelname)s]: %(message)s"

    class Level(enum.Enum):
        NONE = "NONE"
        ERROR = "ERROR"
        WARNING = "WARNING"
        INFO = "INFO"
        DEBUG = "DEBUG"

    def __init__(self, console_level: Level, file_level: Level, log_directory: str):
        self.console_level = self._level_to_logging_level(console_level)
        self.file_level = self._level_to_logging_level(file_level)
        self.directory = log_directory

    @classmethod
    def from_config_file(cls, path=None):
        return cls(cls.Level.INFO, cls.Level.INFO, path)

    def create(self) -> logging.Logger:
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.WARNING)

        # Create a logger
        logger = logging.getLogger("fwutil")
        logger.propagate = False

        # Remove all existing handlers
        for handler in logger.handlers[:]:  # Iterate over a copy of the handler list
            logger.removeHandler(handler)

        logger.setLevel(logging.DEBUG)

        # Add console handler to the logger
        formatter = logging.Formatter(self.FORMAT)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set the log level for the console output
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def _level_to_logging_level(self, level: 'LoggerFactory.Level') -> int:
        mapping = {
            self.Level.NONE: logging.NOTSET,
            self.Level.ERROR: logging.ERROR,
            self.Level.WARNING: logging.WARNING,
            self.Level.INFO: logging.INFO,
            self.Level.DEBUG: logging.DEBUG,
        }
        return mapping[level]
