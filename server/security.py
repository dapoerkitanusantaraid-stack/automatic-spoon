"""Web security helpers for FastAPI applications.

Provides middleware setup for CORS, security headers, and a simple in-memory
rate limiter. Designed to be called from your FastAPI `main` during app setup.
"""
from __future__ import annotations

import time
from typing import Iterable, Optional

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class SimpleRateLimiter(BaseHTTPMiddleware):
    """Basic in-memory rate limiter middleware.

    Not suitable for multi-process production (use Redis-based limiter)
    but useful as a safety layer during development and single-instance
    deployments.
    """

    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        # maps ip -> list of timestamps
        self._hits: dict[str, list[float]] = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        hits = self._hits.setdefault(client_ip, [])
        # remove expired
        while hits and hits[0] <= now - self.window:
            hits.pop(0)
        hits.append(now)
        if len(hits) > self.max_requests:
            return Response(content="Too Many Requests", status_code=429)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to apply common security headers."""

    def __init__(self, app, csp: Optional[str] = None):
        super().__init__(app)
        self.csp = csp

    async def dispatch(self, request: Request, call_next):
        resp = await call_next(request)
        headers = {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "geolocation=()",
        }
        if self.csp:
            headers["Content-Security-Policy"] = self.csp
        for k, v in headers.items():
            resp.headers.setdefault(k, v)
        return resp


def add_security_middleware(app, *, allow_origins: Optional[Iterable[str]] = None,
                            max_requests: int = 200, window_seconds: int = 60,
                            csp: Optional[str] = "default-src 'self';"):
    """Attach security middlewares to FastAPI `app`.

    Usage (in your `main.py`):
        from server.security import add_security_middleware
        add_security_middleware(app, allow_origins=["https://yourdomain.com"])
    """
    # CORS
    allow_origins = list(allow_origins or ["*"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Rate limiting
    app.add_middleware(SimpleRateLimiter, max_requests=max_requests, window_seconds=window_seconds)

    # Security headers
    app.add_middleware(SecurityHeadersMiddleware, csp=csp)


__all__ = ["add_security_middleware", "SimpleRateLimiter", "SecurityHeadersMiddleware"]
