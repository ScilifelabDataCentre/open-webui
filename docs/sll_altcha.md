# Signup verification

Public password signup, including initial administrator signup, now requires a
self-hosted ALTCHA proof of work. The widget is bundled locally and uses
`GET /api/v1/auths/altcha/challenge`; there is no external verification service.
Sign-in, LDAP, OAuth, trusted-header registration, and administrator-created users
continue through their existing flows.

Install the updated frontend/backend dependencies, rebuild the frontend, and
restart the backend. No database changes or migrations are required. Existing
`WEBUI_SECRET_KEY` configuration is used to derive a separate signing key.
HTTPS is required outside localhost for the browser's cryptographic APIs.

Challenges expire after 20 minutes. The server verifies the signature, purpose,
expiration and solution before account creation, then atomically consumes the
issued nonce. A proof is consumed even if subsequent signup validation fails;
the view obtains a fresh proof for retry. Challenge generation and verification each allow 30
requests per minute per client IP, using the existing Redis-backed rate limiter
(per-process fallback when Redis is unavailable).

With Redis configured, issued nonces are stored with a TTL and consumed with
atomic `GETDEL` (Redis 6.2+). Use the same Redis instance, key prefix, and
`WEBUI_SECRET_KEY` across workers. If Redis is configured but unavailable,
verification fails closed with HTTP 503; it never falls back to independent
worker stores.

Without Redis, a bounded in-memory registry supports a single backend worker.
Expiry removes old entries, and consuming a nonce removes it immediately.
Restarting the worker invalidates outstanding challenges. A different worker
will reject a challenge it did not issue, so multi-worker deployments require
Redis. Rejected challenges cannot be replayed after a restart.

API clients calling `POST /api/v1/auths/signup` must include the widget's Base64
payload in the JSON `altcha` field. Missing, invalid, expired and reused proofs
return HTTP 400; throttled requests return HTTP 429.

Most implementation is isolated in `sll_` files. Existing auth files only import
the router/component and pass or verify the payload. Dependencies are pinned to
ALTCHA widget 3.5.0 and Python library 2.3.0 (proof-of-work v2).

Protocol references: [ALTCHA server integration](https://altcha.org/docs/integration/server/)
and the [official Python library](https://github.com/altcha-org/altcha-lib-py).

Run backend regression tests against an isolated database, using the project's
configured Python interpreter:

```sh
ENABLE_DB_MIGRATIONS=false DATABASE_URL=sqlite:////tmp/sll_altcha_tests.db \
  WEBUI_SECRET_KEY=sll-altcha-tests PYTHONPATH=backend \
  .venv/bin/python -m unittest discover -s backend/tests -p 'sll_altcha_test.py' -v
```

The tests cover fresh challenges, valid signup, missing/malformed/tampered proofs,
expiry, purpose binding, concurrent replay, Redis failures, local storage bounds,
cleanup, and throttling. In a browser,
check signup in light/dark mode, submit again after an invalid email/password,
and switch between sign-in and signup to confirm verification resets.
