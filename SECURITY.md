## Security Guide — Web, Bot, and Firewall

This file summarizes recommended and provided security components added to the project.

1) Web application security
- A helper `add_security_middleware(app, ...)` is provided in `server/security.py`.
- It installs:
  - `CORSMiddleware` (configure `allow_origins` explicitly)
  - `SimpleRateLimiter` (in-memory basic rate limiting)
  - `SecurityHeadersMiddleware` (CSP, X-Frame-Options, nosniff, etc.)

Usage (in `main.py`):

```py
from fastapi import FastAPI
from server.security import add_security_middleware

app = FastAPI()
add_security_middleware(app, allow_origins=["https://yourdomain.com"], max_requests=200)
```

2) Bot webhook security
- Helpers in `server/bot_security.py`:
  - `verify_telegram_request(headers, expected_secret)`
  - `verify_facebook_signature(headers, body, app_secret)`
  - `verify_twilio_request(headers, url, params, auth_token)`

Use these in your webhook endpoints to reject unauthenticated requests before processing.

3) Firewall & intrusion prevention
- Script `scripts/setup_firewall.sh` will:
  - Install `ufw` and `fail2ban` (Ubuntu/Debian)
  - Set default deny incoming, allow outgoing
  - Allow SSH, HTTP, HTTPS
  - Configure basic `fail2ban` jail for SSH and nginx

Run as root on the server:

```bash
sudo bash scripts/setup_firewall.sh
```

4) Production notes
- For multi-instance setups use centralized rate-limiting (Redis) and shared logs.
- Use HSM or KMS to store secrets in production; do NOT store `ADMIN_TOKEN` in plain .env in production.
- Enforce HTTPS at load balancer/nginx level and use HTTP Strict Transport Security (HSTS).
- Use official SDKs for Twilio/Facebook/Telegram to verify requests when available.

5) Monitoring & Alerts
- Add Prometheus/Grafana for metrics and alerting on suspicious spikes.
- Aggregate logs to ELK or a log management provider; set alerts for repeated 401/429 events.

6) Next steps (optional)
- Add Redis-backed rate limiter and distributed locking.
- Add automated security scanner (Dependency-Check, Snyk).
- Harden SSH (use key auth, disable password auth, change default port if needed).
