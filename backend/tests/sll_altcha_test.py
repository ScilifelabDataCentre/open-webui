"""Run with PYTHONPATH=backend and an isolated DATABASE_URL (see docs/sll_altcha.md)."""

import asyncio
import base64
import json
import time
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from altcha import Challenge, Payload, create_challenge, solve_challenge
from fastapi import FastAPI, HTTPException, Request, Response
from httpx import ASGITransport, AsyncClient
from open_webui.routers import auths, sll_altcha
from redis.exceptions import ConnectionError as RedisConnectionError


def solved_payload(**overrides):
    options = {
        'algorithm': 'PBKDF2/SHA-256',
        'cost': 1,
        'key_prefix': '00',
        'expires_at': int(time.time()) + 600,
        'data': {'purpose': sll_altcha.PURPOSE},
        'hmac_secret': sll_altcha.signing_key(),
    }
    challenge = create_challenge(**(options | overrides))
    solution = solve_challenge(challenge, timeout=10)
    assert solution is not None
    return Payload(challenge, solution)


class SllAltchaTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.store = sll_altcha.SllAltchaChallengeStore()
        self.store_patch = patch.object(sll_altcha, 'challenge_store', self.store)
        self.store_patch.start()
        self.redis_patch = patch.object(sll_altcha, 'REDIS_URL', '')
        self.redis_patch.start()
        self.key_patch = patch.object(sll_altcha, 'WEBUI_SECRET_KEY', 'sll-altcha-unit-tests')
        self.key_patch.start()
        self.limiter_patch = patch.object(sll_altcha, 'rate_limiter', sll_altcha.RateLimiter(limit=30, window=60))
        self.limiter_patch.start()
        self.app = FastAPI()
        self.app.include_router(sll_altcha.router)
        self.request = Request({'type': 'http', 'app': self.app, 'client': ('127.0.0.1', 1234)})

    async def asyncTearDown(self):
        self.limiter_patch.stop()
        self.key_patch.stop()
        self.redis_patch.stop()
        self.store_patch.stop()

    async def issued_payload(self):
        payload = solved_payload()
        await self.store.issue(None, payload.challenge.parameters.nonce, payload.challenge.parameters.expires_at)
        return payload.to_base64()

    async def test_challenge_endpoint_is_fresh_uncached_and_solvable(self):
        async with AsyncClient(transport=ASGITransport(app=self.app), base_url='http://test') as client:
            first = await client.get('/altcha/challenge')
            second = await client.get('/altcha/challenge')
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.headers['cache-control'], 'no-store')
        self.assertNotEqual(first.json(), second.json())
        challenge = Challenge.from_dict(first.json())
        solution = await asyncio.to_thread(solve_challenge, challenge, timeout=20)
        self.assertIsNotNone(solution)
        sll_altcha.validate_payload(Payload(challenge, solution).to_base64())

    async def test_missing_malformed_and_oversized_payloads_are_rejected(self):
        for encoded in ['', 'invalid', 'a' * 4097] + [
            base64.b64encode(json.dumps(value).encode()).decode()
            for value in [None, [], {}, {'challenge': []}, {'challenge': {}, 'solution': {}}]
        ]:
            with self.subTest(encoded=encoded[:40]), self.assertRaises(HTTPException) as caught:
                sll_altcha.validate_payload(encoded)
            self.assertEqual(caught.exception.status_code, 400)

    async def test_expiry_signature_and_purpose_are_enforced(self):
        for overrides in [
            {'expires_at': int(time.time()) - 1},
            {'expires_at': None},
            {'hmac_secret': 'attacker-key'},
            {'data': {'purpose': 'another_form'}},
        ]:
            with self.subTest(overrides=overrides), self.assertRaises(HTTPException):
                sll_altcha.validate_payload(solved_payload(**overrides).to_base64())

    async def test_tampered_parameters_and_solution_are_rejected(self):
        payload = solved_payload()
        for change in ['expiry', 'cost', 'key', 'counter']:
            modified = Payload.from_base64(payload.to_base64())
            if change == 'expiry':
                modified.challenge.parameters.expires_at += 100
            elif change == 'cost':
                modified.challenge.parameters.cost = 0
            elif change == 'key':
                modified.solution.derived_key = '00' * 32
            else:
                modified.solution.counter = True
            with self.subTest(change=change), self.assertRaises(HTTPException):
                sll_altcha.validate_payload(modified.to_base64())

    async def test_concurrent_replay_has_exactly_one_success(self):
        encoded = await self.issued_payload()
        results = await asyncio.gather(
            *(sll_altcha.verify_signup_altcha(self.request, encoded) for _ in range(3)),
            return_exceptions=True,
        )
        self.assertEqual(results.count(None), 1)
        failures = [result for result in results if isinstance(result, HTTPException)]
        self.assertEqual([error.status_code for error in failures], [400, 400])
        with self.assertRaises(HTTPException):
            await sll_altcha.verify_signup_altcha(self.request, encoded)

    async def test_expired_pending_challenges_are_removed(self):
        self.store.pending['old'] = int(time.time()) - 1
        encoded = await self.issued_payload()
        self.assertNotIn('old', self.store.pending)
        await sll_altcha.verify_signup_altcha(self.request, encoded)
        self.assertEqual(self.store.pending, {})

    async def test_unissued_and_lost_challenges_fail_closed(self):
        with self.assertRaises(HTTPException):
            await sll_altcha.verify_signup_altcha(self.request, solved_payload().to_base64())
        encoded = await self.issued_payload()
        # Simulate a restart or a request landing on another worker without Redis.
        with patch.object(sll_altcha, 'challenge_store', sll_altcha.SllAltchaChallengeStore()):
            with self.assertRaises(HTTPException):
                await sll_altcha.verify_signup_altcha(self.request, encoded)

    async def test_redis_consumption_is_shared_between_workers(self):
        values = {}

        async def store(key, value, *, ex, nx):
            self.assertGreater(ex, 0)
            self.assertTrue(nx)
            if key in values:
                return False
            values[key] = value
            return True

        redis = SimpleNamespace(
            set=AsyncMock(side_effect=store), getdel=AsyncMock(side_effect=lambda key: values.pop(key, None))
        )
        self.app.state.redis = redis
        payload = solved_payload()
        await self.store.issue(redis, payload.challenge.parameters.nonce, payload.challenge.parameters.expires_at)
        with patch.object(sll_altcha, 'challenge_store', sll_altcha.SllAltchaChallengeStore()):
            await sll_altcha.verify_signup_altcha(self.request, payload.to_base64())
        with self.assertRaises(HTTPException):
            await sll_altcha.verify_signup_altcha(self.request, payload.to_base64())
        self.assertEqual(values, {})
        self.assertEqual(self.store.pending, {})

    async def test_redis_outage_does_not_fall_back_to_local_storage(self):
        redis = SimpleNamespace(
            set=AsyncMock(side_effect=RedisConnectionError()),
            getdel=AsyncMock(side_effect=RedisConnectionError()),
        )
        for operation in [self.store.issue(redis, 'nonce', int(time.time()) + 60), self.store.consume(redis, 'nonce')]:
            with self.assertRaises(HTTPException) as caught:
                await operation
            self.assertEqual(caught.exception.status_code, 503)
        self.assertEqual(self.store.pending, {})
        with patch.object(sll_altcha, 'REDIS_URL', 'redis://configured'):
            with self.assertRaises(HTTPException) as caught:
                sll_altcha.redis_client(self.request)
            self.assertEqual(caught.exception.status_code, 503)

    async def test_local_store_is_bounded(self):
        self.store.pending = {str(index): int(time.time()) + 60 for index in range(10000)}
        with self.assertRaises(HTTPException) as caught:
            await self.store.issue(None, 'extra', int(time.time()) + 60)
        self.assertEqual(caught.exception.status_code, 503)

    async def test_rate_limit(self):
        for _ in range(30):
            await sll_altcha.limit_requests(self.request, 'challenge')
        with self.assertRaises(HTTPException) as caught:
            await sll_altcha.limit_requests(self.request, 'challenge')
        self.assertEqual(caught.exception.status_code, 429)
        # Challenge fetches do not consume the signup submission budget.
        await sll_altcha.limit_requests(self.request, 'signup')

    async def test_signup_requires_proof_before_creating_user(self):
        form = sll_altcha.SllSignupForm(name='Test', email='test@example.com', password='test-password')
        with patch.object(auths, 'signup_handler', new_callable=AsyncMock) as create_user:
            with self.assertRaises(HTTPException) as caught:
                await auths.signup(self.request, Response(), form, db=None)
            self.assertEqual(caught.exception.status_code, 400)
            create_user.assert_not_awaited()

    async def test_verified_signup_reaches_existing_account_flow(self):
        form = sll_altcha.SllSignupForm(
            name='Test', email='test@example.com', password='test-password', altcha=await self.issued_payload()
        )
        user = SimpleNamespace(id='test-user', email=form.email)
        with (
            patch.object(auths.Users, 'has_users', AsyncMock(return_value=False)),
            patch.object(auths.Users, 'get_user_by_email', AsyncMock(return_value=None)),
            patch.object(auths.Config, 'get', AsyncMock(return_value=True)),
            patch.object(auths, 'validate_password'),
            patch.object(auths, 'signup_handler', AsyncMock(return_value=user)) as create_user,
            patch.object(auths, 'publish_event', AsyncMock()),
            patch.object(auths, 'create_signin_response', AsyncMock(return_value={'token': 'test-session'})),
        ):
            result = await auths.signup(self.request, Response(), form, db=None)
            self.assertEqual(result, {'token': 'test-session'})
            create_user.assert_awaited_once()
            with self.assertRaises(HTTPException):
                await auths.signup(self.request, Response(), form, db=None)
            create_user.assert_awaited_once()


if __name__ == '__main__':
    unittest.main()
