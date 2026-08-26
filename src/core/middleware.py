import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request process time to headers."""

    async def dispatch(self, request: Request, call_next):
        begin = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - begin

        response.headers["X-Process-Time"] = f"{elapsed:.4f}"
        return response
