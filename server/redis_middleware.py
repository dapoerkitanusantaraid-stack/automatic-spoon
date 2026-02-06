"""Async Redis-backed rate limiting middleware.

This middleware requires `redis.asyncio` installed. It uses a simple fixed
window key approach and is intended for distributed deployments.
"""
from __future__ import annotations

import time
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

try:
    import redis.asyncio as aioredis
except Exception:  # pragma: no cover - import guard
    aioredis = None


class RedisRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str, max_requests: int = 200, window_seconds: int = 60):
        super().__init__(app)
        if aioredis is None:
            raise RuntimeError("redis.asyncio is required for RedisRateLimitMiddleware")
        self.redis = aioredis.from_url(redis_url)
        self.max_requests = max_requests
        self.window = window_seconds

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = int(time.time())
        window_key = f"rl:{client_ip}:{now // self.window}"
        # Atomically increment
        try:
            count = await self.redis.incr(window_key)
            if count == 1:
                await self.redis.expire(window_key, self.window + 1)
        except Exception:
            # If redis is unavailable, allow request (fail-open)
            return await call_next(request)

        if count > self.max_requests:
            return Response(content="Too Many Requests", status_code=429)
        return await call_next(request)
