"""Purpose-bound verification tokens and Gmail delivery for native accounts."""

from __future__ import annotations

import asyncio
import base64
import json
from email.message import EmailMessage
from html import escape
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from open_webui.env import (
    EMAIL_VERIFICATION_TOKEN_TTL,
    EMAIL_VERIFICATION_URL,
    GMAIL_CREDENTIALS_JSON,
    GMAIL_DELEGATED_USER,
    GMAIL_SENDER_EMAIL,
)
from open_webui.utils.auth import create_token, decode_token
from open_webui.utils.misc import parse_duration

GMAIL_SEND_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
TOKEN_PURPOSE = 'email_verification'


class EmailVerificationConfigurationError(ValueError):
    """A required delivery setting is missing or invalid."""


class EmailVerificationDeliveryError(RuntimeError):
    """Gmail could not accept a correctly configured verification email."""


def create_email_verification_token(user_id: str, email: str) -> str:
    try:
        ttl = parse_duration(EMAIL_VERIFICATION_TOKEN_TTL)
    except ValueError as exc:
        raise EmailVerificationConfigurationError('EMAIL_VERIFICATION_TOKEN_TTL is invalid.') from exc

    if ttl is None or ttl.total_seconds() <= 0:
        raise EmailVerificationConfigurationError('EMAIL_VERIFICATION_TOKEN_TTL must be greater than zero.')

    return create_token(
        {'id': user_id, 'email': email.lower(), 'purpose': TOKEN_PURPOSE},
        expires_delta=ttl,
    )


def decode_email_verification_token(token: str) -> dict | None:
    data = decode_token(token)
    if not data or data.get('purpose') != TOKEN_PURPOSE:
        return None
    if not isinstance(data.get('id'), str) or not isinstance(data.get('email'), str):
        return None
    return data


def build_verification_link(token: str, verification_url: str) -> str:
    if not verification_url:
        raise EmailVerificationConfigurationError(
            'EMAIL_VERIFICATION_URL or WEBUI_URL must be configured with a public URL.'
        )

    parts = urlsplit(verification_url)
    if parts.scheme not in {'http', 'https'} or not parts.netloc:
        raise EmailVerificationConfigurationError('EMAIL_VERIFICATION_URL must be an absolute HTTP(S) URL.')

    query = parse_qsl(parts.query, keep_blank_values=True)
    query.append(('token', token))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def build_verification_message(recipient: str, verification_link: str) -> EmailMessage:
    message = EmailMessage()
    message['To'] = recipient
    message['From'] = GMAIL_SENDER_EMAIL
    message['Subject'] = 'Verify your email address'
    message.set_content(
        'Verify your email address to finish creating your Open WebUI account:\n\n'
        f'{verification_link}\n\n'
        'This link expires after the configured verification period.'
    )
    html_verification_link = escape(verification_link, quote=True)
    message.add_alternative(
        '<p>Verify your email address to finish creating your Open WebUI account.</p>'
        f'<p><a href="{html_verification_link}">Verify email address</a></p>'
        '<p>This link expires after the configured verification period.</p>',
        subtype='html',
    )
    return message


def _gmail_credentials():
    if not GMAIL_SENDER_EMAIL or not GMAIL_CREDENTIALS_JSON:
        raise EmailVerificationConfigurationError(
            'GMAIL_SENDER_EMAIL and GMAIL_CREDENTIALS_JSON are required when email verification is enabled.'
        )

    try:
        credential_info = json.loads(GMAIL_CREDENTIALS_JSON)
    except json.JSONDecodeError as exc:
        raise EmailVerificationConfigurationError('GMAIL_CREDENTIALS_JSON must contain valid JSON.') from exc

    if not isinstance(credential_info, dict):
        raise EmailVerificationConfigurationError('GMAIL_CREDENTIALS_JSON must contain a JSON object.')

    is_service_account = credential_info.get('type') == 'service_account'

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials

        if is_service_account:
            if not GMAIL_DELEGATED_USER:
                raise EmailVerificationConfigurationError(
                    'GMAIL_DELEGATED_USER is required when using service-account credentials.'
                )
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_info(
                credential_info, scopes=[GMAIL_SEND_SCOPE]
            ).with_subject(GMAIL_DELEGATED_USER)
        else:
            credentials = Credentials.from_authorized_user_info(credential_info, scopes=[GMAIL_SEND_SCOPE])

        # Authorized-user credentials refresh with their refresh token; service
        # accounts obtain their first access token through the same refresh API.
        if not credentials.valid:
            try:
                credentials.refresh(Request())
            except Exception as exc:
                if is_service_account:
                    raise EmailVerificationConfigurationError(
                        'Gmail service-account refresh failed. Authorize this service account client ID for '
                        'Google Workspace domain-wide delegation with the gmail.send scope.'
                    ) from exc
                raise EmailVerificationConfigurationError('Gmail credentials could not be refreshed.') from exc
        if not credentials.valid:
            raise EmailVerificationConfigurationError('Gmail credentials are expired or invalid.')
        return credentials
    except EmailVerificationConfigurationError:
        raise
    except Exception as exc:
        raise EmailVerificationConfigurationError('Gmail credentials could not be loaded.') from exc


def _send_message(message: EmailMessage) -> None:
    try:
        from googleapiclient.discovery import build

        credentials = _gmail_credentials()
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode('ascii')
        build('gmail', 'v1', credentials=credentials, cache_discovery=False).users().messages().send(
            userId='me', body={'raw': encoded_message}
        ).execute()
    except EmailVerificationConfigurationError:
        raise
    except Exception as exc:
        raise EmailVerificationDeliveryError('Gmail delivery failed.') from exc


async def send_email_verification(recipient: str, user_id: str, verification_url: str) -> None:
    token = create_email_verification_token(user_id, recipient)
    link = build_verification_link(token, verification_url)
    message = build_verification_message(recipient, link)
    await asyncio.to_thread(_send_message, message)
