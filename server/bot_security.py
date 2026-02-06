"""Helpers to verify bot webhook requests (Telegram, Twilio, Facebook).

These functions provide basic signature/token checks for incoming webhooks.
They are not a replacement for full SDKs but help validate authenticity.
"""
from __future__ import annotations

import hmac
import hashlib
from typing import Mapping, Optional


def verify_telegram_request(headers: Mapping[str, str], expected_secret: Optional[str]) -> bool:
    """Verify Telegram webhook using `X-Telegram-Bot-Api-Secret-Token` header.

    If `expected_secret` is None, verification will fail (safer to require secret).
    """
    if not expected_secret:
        return False
    header = headers.get("X-Telegram-Bot-Api-Secret-Token") or headers.get("x-telegram-bot-api-secret-token")
    return bool(header) and hmac.compare_digest(header, expected_secret)


def verify_facebook_signature(headers: Mapping[str, str], body: bytes, app_secret: Optional[str]) -> bool:
    """Verify Facebook Graph webhook signature (X-Hub-Signature or X-Hub-Signature-256).

    Supports HMAC-SHA1 (`sha1=`) and HMAC-SHA256 (`sha256=`).
    """
    if not app_secret:
        return False
    sig = headers.get("X-Hub-Signature-256") or headers.get("x-hub-signature-256") or headers.get("X-Hub-Signature")
    if not sig:
        return False
    if sig.startswith("sha1="):
        expected = hmac.new(app_secret.encode(), body, hashlib.sha1).hexdigest()
        return hmac.compare_digest(sig.split("=", 1)[1], expected)
    if sig.startswith("sha256="):
        expected = hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(sig.split("=", 1)[1], expected)
    return False


def verify_twilio_request(headers: Mapping[str, str], url: str, params: Mapping[str, str], auth_token: Optional[str]) -> bool:
    """Basic Twilio request validator using X-Twilio-Signature.

    Twilio signs the full URL and parameters. For robust validation use
    Twilio's official helper libraries; this is a simplified implementation.
    """
    if not auth_token:
        return False
    signature = headers.get("X-Twilio-Signature") or headers.get("x-twilio-signature")
    if not signature:
        return False
    # Build validation string: url + sorted params
    items = "".join(f"{k}{params[k]}" for k in sorted(params))
    data = (url + items).encode()
    expected = hmac.new(auth_token.encode(), data, hashlib.sha1).digest()
    import base64

    expected_b64 = base64.b64encode(expected).decode()
    return hmac.compare_digest(signature, expected_b64)


__all__ = [
    "verify_telegram_request",
    "verify_facebook_signature",
    "verify_twilio_request",
]
