"""Self-hosted ALTCHA challenges and single-use verification for public signup."""

import hmac
import time

from altcha import Payload, create_challenge, verify_solution
from fastapi import APIRouter, HTTPException, Request, Response
from open_webui.env import REDIS_KEY_PREFIX, REDIS_URL, WEBUI_SECRET_KEY
from open_webui.models.auths import SignupForm
from open_webui.utils.rate_limit import RateLimiter
from pydantic import Field
from redis.exceptions import RedisError
from starlette.concurrency import run_in_threadpool

CHALLENGE_SECONDS = 1200
PURPOSE = 'sll_signup'
INVALID_MESSAGE = 'Please complete the signup verification again.'
router = APIRouter()
rate_limiter = RateLimiter(limit=30, window=60)


class SllSignupForm(SignupForm):
    altcha: str = Field(default='', max_length=4096)


class SllAltchaChallengeStore:
    """Only issued challenges can be consumed; local proofs fail closed on other workers."""

    def __init__(self):
        self.pending: dict[str, int] = {}

    def prune(self):
        now = int(time.time())
        self.pending = {nonce: expiry for nonce, expiry in self.pending.items() if expiry > now}

    async def issue(self, redis, nonce: str, expires_at: int) -> None:
        if redis is not None:
            try:
                stored = await redis.set(
                    f'{REDIS_KEY_PREFIX}:sll_altcha:{nonce}', '1', ex=expires_at - int(time.time()), nx=True
                )
            except RedisError as error:
                raise HTTPException(503, 'Signup verification is temporarily unavailable.') from error
            if not stored:
                raise HTTPException(503, 'Signup verification is temporarily unavailable.')
        else:
            self.prune()
            if len(self.pending) >= 10000:
                raise HTTPException(503, 'Signup verification is temporarily unavailable.')
            self.pending[nonce] = expires_at

    async def consume(self, redis, nonce: str) -> None:
        if redis is not None:
            try:
                consumed = await redis.getdel(f'{REDIS_KEY_PREFIX}:sll_altcha:{nonce}')
            except RedisError as error:
                raise HTTPException(503, 'Signup verification is temporarily unavailable.') from error
        else:
            self.prune()
            # No await between checking and removing: atomic within this worker.
            consumed = self.pending.pop(nonce, None)
        if not consumed:
            raise HTTPException(400, INVALID_MESSAGE)


challenge_store = SllAltchaChallengeStore()


def redis_client(request: Request):
    redis = getattr(request.app.state, 'redis', None)
    if REDIS_URL and redis is None:
        raise HTTPException(503, 'Signup verification is temporarily unavailable.')
    return redis


def signing_key() -> bytes:
    if not WEBUI_SECRET_KEY:
        raise HTTPException(503, 'Signup verification is temporarily unavailable.')
    return hmac.digest(WEBUI_SECRET_KEY.encode(), b'sll_altcha_signup', 'sha256')


async def limit_requests(request: Request, action: str) -> None:
    ip = request.client.host if request.client else 'unknown'
    if await rate_limiter.is_limited(getattr(request.app.state, 'redis', None), f'sll_altcha:{action}:{ip}'):
        raise HTTPException(
            429, 'Too many verification attempts. Please try again later.', headers={'Retry-After': '60'}
        )


@router.get('/altcha/challenge')
async def signup_challenge(request: Request, response: Response):
    await limit_requests(request, 'challenge')
    response.headers['Cache-Control'] = 'no-store'
    challenge = create_challenge(
        algorithm='PBKDF2/SHA-256',
        cost=5000,
        key_prefix='00',
        expires_at=int(time.time()) + CHALLENGE_SECONDS,
        data={'purpose': PURPOSE},
        hmac_secret=signing_key(),
    )
    await challenge_store.issue(redis_client(request), challenge.parameters.nonce, challenge.parameters.expires_at)
    return challenge.to_dict()


def validate_payload(encoded: str) -> Payload:
    key = signing_key()
    try:
        if not encoded or len(encoded) > 4096:
            raise ValueError('Missing or oversized payload')
        payload = Payload.from_base64(encoded)
        parameters = payload.challenge.parameters
        if (
            parameters.data != {'purpose': PURPOSE}
            or type(parameters.expires_at) is not int
            or not int(time.time()) < parameters.expires_at <= int(time.time()) + CHALLENGE_SECONDS
            or not verify_solution(payload, key).verified
        ):
            raise ValueError('Invalid solution')
        return payload
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError, RecursionError) as error:
        raise HTTPException(400, INVALID_MESSAGE) from error


async def verify_signup_altcha(request: Request, encoded: str) -> None:
    await limit_requests(request, 'signup')
    payload = await run_in_threadpool(validate_payload, encoded)
    # Consume before account creation, including when later signup validation fails.
    await challenge_store.consume(redis_client(request), payload.challenge.parameters.nonce)
