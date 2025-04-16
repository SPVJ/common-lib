import json
import logging
import time

from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

from fsCommonLib.logs.logger import RequestIdFilter, logger


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, logger: logging.Logger,
                 time_format: str = "%H:%M:%S",
                 time_zone: str = "Local" ):
        super().__init__(app)
        self.logger = logger
        self.time_format = time_format
        self.time_zone = time_zone

    async def dispatch(self, request: Request, call_next):
        timestamp = time.strftime(self.time_format)

        request_body = await request.body()
        request_body_decoded = ""
        logger.info(request_body)
        if request_body != None:
            request_body_decoded = json.loads(request_body.decode('utf-8'))

        request_info = {
            "timestamp": timestamp,
            "request_body": dict(request.headers),
            "request_body" : request_body_decoded,
            "type": "TELEMETRY",
            "hostname": request.client.host,
            "ip": request.client.host,
            "method": request.method,
            "path": request.url.path,
            "url": str(request.url),
        }

        self.logger.info(f"Request {request_info}")

        start_time = time.time()

        response = await call_next(request)
        process_time = time.time() - start_time

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response = Response(content=response_body, status_code=response.status_code, headers=dict(response.headers),
                            media_type=response.media_type)

        response_info = {
            "timestamp": timestamp,
            "latency": f"{process_time:.2f} seconds",
            "status_code": response.status_code,
            "response_body": response_body.decode('utf-8'),
            "type": "TELEMETRY"
        }
        self.logger.info(f"Success {response_info}")

        return response
    
def addLoggingMiddleware(app: FastAPI):
    app.add_middleware(LogMiddleware, logger=logger)
    return app
