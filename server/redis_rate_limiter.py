"""Redis-backed rate limiter for distributed deployments.

Usage:
    limiter = RedisRateLimiter(redis_client, max_requests=200, window_seconds=60)
    allowed = await limiter.allow_request(client_id)

This is asynchronous and requires `aioredis` or `redis.asyncio`.
"""
from __future__ import annotations

import time
from typing import Optional

try:
    import redis.asyncio as aioredis
except Exception:  # pragma: no cover - import guard
    aioredis = None


class RedisRateLimiter:
    def __init__(self, redis_client, max_requests: int = 200, window_seconds: int = 60):
        if aioredis is None:
            raise RuntimeError("redis.asyncio is required for RedisRateLimiter")
        self.redis = redis_client
        self.max_requests = max_requests
        self.window = window_seconds

    async def allow_request(self, key: str) -> bool:
        """Return True if request is allowed; False if rate limited."""
        now = int(time.time())
        window_key = f"rl:{key}:{now // self.window}"
        # Use INCR and EXPIRE atomically
        count = await self.redis.incr(window_key)
        if count == 1:
            await self.redis.expire(window_key, self.window + 1)
        return count <= self.max_requests
