# Signup verification (ALTCHA)

Password signup, including the first admin signup, requires a self-hosted ALTCHA
proof of work. Sign-in, LDAP, OAuth, trusted-header and admin-created users are
unaffected.

## How it works

1. The signup form (`src/lib/components/auth/sll_Altcha.svelte`) fetches a challenge
   from `GET /api/v1/auths/altcha/challenge` and solves it in the browser.
2. `POST /api/v1/auths/signup` sends the solution in the `altcha` field.
3. `backend/open_webui/routers/sll_altcha.py` verifies the signature, purpose,
   expiry (20 min) and solution, then consumes the challenge before the account
   is created. Failed signups need a fresh proof; the widget fetches one automatically.

The signing key is derived from `WEBUI_SECRET_KEY`. Both endpoints are rate-limited
to 30 requests/min per client IP. Invalid, expired or reused proofs return 400,
throttled requests 429.

## Storage

- **Redis** (`REDIS_URL` set): issued challenges are stored with a TTL and consumed
  with `GETDEL` (Redis 6.2+). If Redis is unavailable, signup fails with 503.
- **No Redis**: in-memory store, valid only for a single backend worker. Restarts
  invalidate outstanding challenges.

## Requirements

HTTPS outside localhost (the widget uses browser crypto APIs). Dependencies:
`altcha==2.3.0` (Python), `altcha@3.5.0` (npm).

## Tests

```sh
cd backend && ../.venv/bin/python -m pytest tests/sll_altcha_test.py -q
```
