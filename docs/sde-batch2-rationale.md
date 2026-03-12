# SDE countermeasures batch 2 — status and rationale notes

Apply these in SDElements (project 31763) when the add_countermeasure_note / update flow is available.

## 31763-T536 — Restrict the size of incoming messages in services
- **Status:** Complete (DONE)
- **Rationale note:** Complete: Implemented request body size limit via Flask MAX_CONTENT_LENGTH (default 1 MiB), configurable with MAX_CONTENT_LENGTH env. Flask returns 413 Payload Too Large for oversized requests. Constraint: single app process; reverse proxy may enforce additional limits in production.

## 31763-T1362 — Perform message throttling in Web APIs
- **Status:** Complete (DONE)
- **Rationale note:** Complete: Message throttling implemented for AI endpoints (per-IP and per-user rate limits) and for authentication via account lockout (T70) after failed login attempts. General read APIs are not throttled to preserve training/demo scenarios. Dependency: in-memory rate limit store (per-process).

## 31763-T151 — Use cryptographically secure random numbers
- **Status:** Complete (DONE)
- **Rationale note:** Complete: Replaced random module with secrets for all security-sensitive values: account numbers, card numbers, CVV, reset PINs (all variants), and upload filename prefixes. No constraint; Python 3.6+ secrets module used throughout.

## 31763-T76 — Do not hardcode passwords
- **Status:** Complete (DONE)
- **Rationale note:** Complete: Flask secret_key and JWT_SECRET read from env (FLASK_SECRET_KEY, SECRET_KEY, JWT_SECRET); fallback only for dev/training. database.py already uses DB_PASSWORD from env. Constraint: fallback value retained for local/training use; production should set env and omit fallback.

## 31763-T70 — Implement account lockout or authentication throttling
- **Status:** Complete (DONE)
- **Rationale note:** Complete: Account lockout after 5 failed attempts (LOGIN_FAILURE_MAX), 15 min lockout (LOGIN_LOCKOUT_SECONDS); applied to web login and API login; in-memory store (per-process). Configurable via env. Constraint: in-memory state does not persist across restarts or multiple app workers.
