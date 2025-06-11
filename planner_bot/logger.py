import logging
import sys
from contextvars import ContextVar

request_id: ContextVar[str | None] = ContextVar("request_id", default=None)

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        rid = request_id.get()
        record.request_id = rid if rid else "-"
        return True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)
logger.addFilter(RequestIdFilter())
