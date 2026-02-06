"""Safe function implementations (simple + auth+audit).

This module provides two safe variants:
- `simple_handle_request(run_secret: bool)` - explicit boolean flag
- `auth_handle_request(auth_token: Optional[str])` - token-based authorization with audit logging

Do NOT use hidden checks like `if "backdoor_access" in locals()`; always use
explicit authorization and audit trails for sensitive operations.
"""
from __future__ import annotations

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

# Optionally load environment variables from a .env file when available.
# This allows running the module locally with an ADMIN_TOKEN in a .env file.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; if not installed or .env missing, proceed silently
    pass


def secret_function() -> None:
    """Operasi sistem kritis — hanya untuk user yang berwenang."""
    print("Menjalankan operasi kritis...")


def normal_function() -> None:
    """Tugas sehari-hari non-kritis."""
    print("Menjalankan tugas normal...")


def simple_handle_request(run_secret: bool = False) -> None:
    """Versi sederhana: jalankan fungsi kritis hanya jika flag True.

    Args:
        run_secret: Jika True, panggil `secret_function()`.
    """
    if run_secret:
        secret_function()
    else:
        normal_function()


def setup_audit_logger(path: str = "audit.log") -> logging.Logger:
    """Konfigurasi logger audit dengan rotating file handler.

    Returns a logger instance named 'project_audit'. Multiple calls
    will reuse existing handlers.
    """
    logger = logging.getLogger("project_audit")
    logger.setLevel(logging.INFO)
    # If there's already a RotatingFileHandler for this exact path, reuse it.
    abs_path = os.path.abspath(path)
    for h in logger.handlers:
        if isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == abs_path:
            return logger

    # Otherwise add a new handler specific to this path.
    handler = RotatingFileHandler(path, maxBytes=10 * 1024 * 1024, backupCount=5)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger


def is_authorized(token: Optional[str]) -> bool:
    """Simple token check against `ADMIN_TOKEN` env var.

    In production, replace this with a secure auth system (JWT, OAuth, RBAC).
    """
    admin_token = os.getenv("ADMIN_TOKEN")
    return bool(admin_token) and token == admin_token


def auth_handle_request(auth_token: Optional[str] = None, logger: Optional[logging.Logger] = None) -> None:
    """Authorized handler that logs audit events.

    Args:
        auth_token: Token supplied by caller to authorize critical action.
        logger: Optional logger instance; if None, a default rotating logger is used.
    """
    logger = logger or setup_audit_logger()
    if auth_token and is_authorized(auth_token):
        logger.info("authorized_access: secret_function invoked")
        secret_function()
    else:
        logger.info("unauthorized_or_normal: normal_function invoked")
        normal_function()


if __name__ == "__main__":
    # Demo usage
    print("Demo: simple_handle_request(False)")
    simple_handle_request(False)
    print("Demo: simple_handle_request(True)")
    simple_handle_request(True)

    print('\nDemo: auth_handle_request without token')
    auth_handle_request(None)

    print('\nDemo: auth_handle_request with wrong token')
    auth_handle_request("wrong-token")

    # Demo with environment token
    os.environ["ADMIN_TOKEN"] = "demo-secret"
    print('\nDemo: auth_handle_request with correct token (demo-secret)')
    auth_handle_request("demo-secret")

    print('\nAudit log written to audit.log (check the repository root)')
