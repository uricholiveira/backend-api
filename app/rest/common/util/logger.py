import logging

from app.core.settings import settings


class CustomLogger:
    def __init__(self, log_level: str = settings.util.log.level):
        self.logger: logging.Logger = logging.getLogger(__class__.__name__)
        self.init_logger(log_level=log_level)

    def init_logger(self, log_level: str) -> None:
        format = logging.Formatter("%(levelname)s: \t  %(message)s")
        self.logger.setLevel(level=log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level=log_level)
        console_handler.setFormatter(fmt=format)

        file_handler = logging.FileHandler("development.log")
        file_handler.setLevel(level=log_level)
        file_handler.setFormatter(fmt=format)

        self.logger.addHandler(hdlr=console_handler)
        self.logger.addHandler(hdlr=file_handler)

    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(msg=message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(msg=message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        self.logger.warning(msg=message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        self.logger.error(msg=message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        self.logger.critical(msg=message, *args, **kwargs)
