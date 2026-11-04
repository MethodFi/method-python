"""Verify that incoming webhook requests came from Method.

See https://docs.methodfi.com/reference/webhooks/overview#authentication
"""
import base64
import hashlib
import hmac
import json
import re
import time
from typing import Any, Dict, Mapping, Optional, Union


WEBHOOK_SIGNATURE_HEADER = 'method-webhook-signature'
WEBHOOK_TIMESTAMP_HEADER = 'method-webhook-timestamp'
WEBHOOK_DELIVERY_ID_HEADER = 'method-webhook-delivery-id'
DEFAULT_WEBHOOK_TOLERANCE_SECONDS = 300
_TIMESTAMP_RE = re.compile(r'[0-9]{1,12}')


class MethodWebhookVerificationError(ValueError):
    """Raised when a webhook request cannot be verified. ``code`` says why."""

    def __init__(self, code: str, message: str):
        super(MethodWebhookVerificationError, self).__init__(message)
        self.code = code
        self.message = message


def _get_header(headers: Mapping[str, Any], name: str) -> Optional[str]:
    # Works with dicts, Flask/Werkzeug and Django headers, and case-insensitive mappings.
    for key in headers.keys():
        if key.lower() == name:
            value = headers[key]
            if isinstance(value, (list, tuple)):
                return value[0] if value else None
            return value
    return None


def _to_bytes(payload: Union[str, bytes]) -> bytes:
    return payload.encode('utf-8') if isinstance(payload, str) else payload


def compute_webhook_signature(payload: Union[str, bytes], timestamp: Union[str, int], hmac_secret: str) -> str:
    """HMAC-SHA256 hex digest of ``"{timestamp}:{payload}"`` keyed with the webhook's hmac_secret."""
    message = ('%s:' % timestamp).encode('utf-8') + _to_bytes(payload)
    return hmac.new(hmac_secret.encode('utf-8'), message, hashlib.sha256).hexdigest()


def construct_webhook_event(
    payload: Union[str, bytes],
    headers: Mapping[str, Any],
    hmac_secret: Optional[str] = None,
    auth_token: Optional[str] = None,
    tolerance_seconds: int = DEFAULT_WEBHOOK_TOLERANCE_SECONDS,
    now: Optional[float] = None,
) -> Dict[str, Any]:
    """Verify a webhook request and return ``{'payload', 'delivery_id', 'timestamp'}``.

    Checks the ``Authorization`` header when ``auth_token`` is given, the
    ``method-webhook-signature`` HMAC when ``hmac_secret`` is given (at least one is
    required), and that ``method-webhook-timestamp`` is within ``tolerance_seconds``
    (0 skips the check). ``payload`` must be the raw request body. Does not call the API.

    Raises MethodWebhookVerificationError if the request cannot be verified.
    """
    if not hmac_secret and not auth_token:
        raise MethodWebhookVerificationError(
            'missing_secret', 'Provide the webhook hmac_secret and/or auth_token to verify a webhook.')

    raw_timestamp = _get_header(headers, WEBHOOK_TIMESTAMP_HEADER)
    if raw_timestamp is None:
        raise MethodWebhookVerificationError('missing_header', 'Missing %s header.' % WEBHOOK_TIMESTAMP_HEADER)
    raw_timestamp = raw_timestamp.strip()
    # ASCII digits only, bounded: str.isdigit() accepts characters like '\u00b2' that int() rejects,
    # and very long digit strings hit Python's int conversion limit.
    if not _TIMESTAMP_RE.fullmatch(raw_timestamp):
        raise MethodWebhookVerificationError(
            'invalid_timestamp', '%s must be a UNIX timestamp in seconds.' % WEBHOOK_TIMESTAMP_HEADER)
    timestamp = int(raw_timestamp)

    if auth_token:
        authorization = _get_header(headers, 'authorization')
        if authorization is None:
            raise MethodWebhookVerificationError('missing_header', 'Missing Authorization header.')
        expected = base64.b64encode(auth_token.encode('utf-8')).decode('ascii')
        if not hmac.compare_digest(authorization.strip().encode('utf-8'), expected.encode('utf-8')):
            raise MethodWebhookVerificationError(
                'invalid_authorization', 'Authorization header does not match the webhook auth_token.')

    if hmac_secret:
        signature = _get_header(headers, WEBHOOK_SIGNATURE_HEADER)
        if signature is None:
            raise MethodWebhookVerificationError('missing_header', 'Missing %s header.' % WEBHOOK_SIGNATURE_HEADER)
        expected = compute_webhook_signature(payload, raw_timestamp, hmac_secret)
        if not hmac.compare_digest(signature.strip().lower().encode('utf-8'), expected.encode('utf-8')):
            raise MethodWebhookVerificationError(
                'invalid_signature',
                '%s does not match the payload. Make sure you pass the raw request body.' % WEBHOOK_SIGNATURE_HEADER)

    # Checked after the signature, so an unsigned or tampered request always fails as invalid_signature.
    if tolerance_seconds and tolerance_seconds > 0:
        current = time.time() if now is None else now
        if abs(current - timestamp) > tolerance_seconds:
            raise MethodWebhookVerificationError(
                'timestamp_out_of_tolerance',
                '%s is more than %d seconds from the current time.' % (WEBHOOK_TIMESTAMP_HEADER, tolerance_seconds))

    try:
        parsed = json.loads(_to_bytes(payload).decode('utf-8'))
    except ValueError:
        raise MethodWebhookVerificationError('invalid_payload', 'Webhook payload is not valid JSON.')

    return {
        'payload': parsed,
        'delivery_id': _get_header(headers, WEBHOOK_DELIVERY_ID_HEADER),
        'timestamp': timestamp,
    }
