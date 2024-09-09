import enum
import logging
import sys
from logging.handlers import RotatingFileHandler

_logger = None


class Logger(logging.Logger):
    MAX_FILE_SIZE = 5 * 10**6
    FORMAT = "[%(asctime)s][%(threadName)s][%(name)s.%(funcName)s:%(lineno)s][%(levelname)s]: %(message)s"

    class Level(str, enum.Enum):
        NONE = "NONE"
        ERROR = "ERROR"
        WARNING = "WARNING"
        INFO = "INFO"
        DEBUG = "DEBUG"

    @classmethod
    def get(cls):
        global _logger
        if not _logger:
            _logger = cls()
        return _logger

    @classmethod
    def configure(cls, console_level: Level = Level.INFO):
        logger = cls.get()
        logger.setup_console(console_level)

    def __init__(self):
        super().__init__("fwutil")
        self._console_logger = None
        self._file_logger = None

    def setup_console(self, level: Level):
        # Configure Console Logger
        level_value = self._level_to_logging_level(level)
        formatter = logging.Formatter(self.FORMAT)
        console_logger = logging.StreamHandler(sys.stdout)
        console_logger.setLevel(level_value)
        console_logger.setFormatter(formatter)
        self.addHandler(console_logger)
        self._console_logger = console_logger

    def setup_file(self, level: Level, path: str, max_size=MAX_FILE_SIZE):
        # Configure File Logger
        level_value_file = self._level_to_logging_level(level)
        formatter = logging.Formatter(self.FORMAT)
        file_handler = RotatingFileHandler(path, maxBytes=max_size, backupCount=1)
        file_handler.setLevel(level_value_file)
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

    def _level_to_logging_level(self, level: Level) -> int:
        mapping = {
            self.Level.NONE: logging.NOTSET,
            self.Level.ERROR: logging.ERROR,
            self.Level.WARNING: logging.WARNING,
            self.Level.INFO: logging.INFO,
            self.Level.DEBUG: logging.DEBUG,
        }
        return mapping[level]
