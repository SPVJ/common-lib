import logging
from pythonjsonlogger.json import JsonFormatter


class RequestIdFilter(logging.Filter):
    def __init__(self, correlation_id: str):
        super().__init__()
        self.correlation_id = correlation_id

    def filter(self, record):
        record.correlation_id = self.correlation_id
        return True


logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
log_formatter = JsonFormatter(
    "{levelname} : {message}",
    style="{",
)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
