# Safe Functions Utility

This module provides safe implementations for running critical and non-critical
functions without hidden backdoors.

Files:

- `server/safe_functions.py`: two safe handlers:
  - `simple_handle_request(run_secret: bool)` — explicit boolean flag to run the critical function
  - `auth_handle_request(auth_token: Optional[str])` — token-based authorization with audit logging

Usage:

1. Option A — simple flag:

```py
from server.safe_functions import simple_handle_request

simple_handle_request(True)  # runs secret_function
```

2. Option B — token-based (recommended for production):

- Set `ADMIN_TOKEN` in environment or in a `.env` file (module attempts to load `.env` if `python-dotenv` is installed).

```bash
export ADMIN_TOKEN="supersecret"
python3 -c "from server.safe_functions import auth_handle_request; auth_handle_request('supersecret')"
```

Audit logs:

- By default logs are written to `audit.log` in the current working directory and rotated.
- You can pass a custom logger or path using `setup_audit_logger(path)`.

Security notes:

- Do NOT use hidden checks such as `if 'backdoor_access' in locals()`.
- Use explicit authorization (JWT/OAuth/RBAC) in production and keep audit trails for sensitive operations.
