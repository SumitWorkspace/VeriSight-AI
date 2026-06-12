from __future__ import annotations

import logging
import threading
import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("fake_review_api")

class SlidingWindowRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, requests_limit: int = 100, window_seconds: int = 60) -> None:
        super().__init__(app)
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self.client_timestamps: dict[str, list[float]] = {}
        self.lock = threading.Lock()

    async def dispatch(self, request: Request, call_next):
        # Retrieve client IP, fallback to loopback
        client_ip = request.client.host if request.client else "127.0.0.1"
        current_time = time.time()

        with self.lock:
            # Get existing timestamps and purge expired entries
            timestamps = self.client_timestamps.get(client_ip, [])
            cutoff_time = current_time - self.window_seconds
            valid_timestamps = [t for t in timestamps if t > cutoff_time]

            # Check if threshold is breached
            if len(valid_timestamps) >= self.requests_limit:
                logger.warning(
                    "Rate limit exceeded for IP %s on %s",
                    client_ip,
                    request.url.path,
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Too Many Requests",
                        "detail": f"Rate limit exceeded. Please limit requests to {self.requests_limit} per {self.window_seconds} seconds.",
                        "path": request.url.path,
                    },
                )

            # Record current transaction
            valid_timestamps.append(current_time)
            self.client_timestamps[client_ip] = valid_timestamps

        return await call_next(request)
