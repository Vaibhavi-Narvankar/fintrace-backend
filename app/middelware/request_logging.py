import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger(__name__)

async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        process_time = (time.perf_counter() - start_time) * 1000

        logger.info(
            "request_completed | request_id=%s | method=%s | path=%s | status_code=%s | duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time
        )

        response.headers["X-Request-ID"] = request_id

        return response

    except Exception:
        process_time = (time.perf_counter() - start_time) * 1000

        logger.error(
            "request_failed | request_id=%s | method=%s | path=%s | duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            process_time
        )

        raise