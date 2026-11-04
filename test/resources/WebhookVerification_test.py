"""Offline tests for webhook verification (no API key or network needed)."""
import base64
import hashlib
import hmac
import json

import pytest

from method import Method, MethodWebhookVerificationError, compute_webhook_signature, construct_webhook_event

HMAC_SECRET = 'whsec_test_secret'
AUTH_TOKEN = 'test-auth-token'
NOW = 1730000000
PAYLOAD = json.dumps({
    'webhook_id': 'whk_cSGjA6d9N8y8R',
    'id': 'acc_BcRdHNjb9TYKV',
    'type': 'account.update',
    'op': 'update',
    'path': '/accounts/acc_BcRdHNjb9TYKV',
    'event': 'evt_knqJgxKUnqDVJ',
    'refs': {'account': 'acc_BcRdHNjb9TYKV', 'entity': 'ent_qKNBB68bfHGNA'},
})


def docs_signature(payload, timestamp, secret):
    # Same recipe as the docs: HMAC-SHA256 hex of "{timestamp}:{raw body}".
    return hmac.new(secret.encode(), ('%s:%s' % (timestamp, payload)).encode(), hashlib.sha256).hexdigest()


def signed_headers(**overrides):
    headers = {
        'method-webhook-timestamp': str(NOW),
        'method-webhook-signature': docs_signature(PAYLOAD, NOW, HMAC_SECRET),
        'method-webhook-delivery-id': 'dlv_123',
        'authorization': base64.b64encode(AUTH_TOKEN.encode()).decode(),
    }
    for key, value in overrides.items():
        key = key.replace('_', '-')
        if value is None:
            headers.pop(key, None)
        else:
            headers[key] = value
    return headers


def assert_code(code, **kwargs):
    with pytest.raises(MethodWebhookVerificationError) as info:
        construct_webhook_event(**kwargs)
    assert info.value.code == code


def test_signature_matches_documented_recipe():
    assert compute_webhook_signature(PAYLOAD, NOW, HMAC_SECRET) == docs_signature(PAYLOAD, NOW, HMAC_SECRET)
    assert compute_webhook_signature(PAYLOAD.encode(), str(NOW), HMAC_SECRET) == docs_signature(PAYLOAD, NOW, HMAC_SECRET)


def test_valid_request_returns_event_delivery_id_and_timestamp():
    event = construct_webhook_event(PAYLOAD, signed_headers(), hmac_secret=HMAC_SECRET, auth_token=AUTH_TOKEN, now=NOW + 10)
    assert event['payload']['type'] == 'account.update'
    assert event['payload']['refs']['entity'] == 'ent_qKNBB68bfHGNA'
    assert event['delivery_id'] == 'dlv_123'
    assert event['timestamp'] == NOW


def test_bytes_body_and_mixed_case_headers():
    headers = {'Method-Webhook-Timestamp': str(NOW), 'METHOD-WEBHOOK-SIGNATURE': [signed_headers()['method-webhook-signature']]}
    event = construct_webhook_event(PAYLOAD.encode(), headers, hmac_secret=HMAC_SECRET, now=NOW)
    assert event['payload']['id'] == 'acc_BcRdHNjb9TYKV'
    assert event['delivery_id'] is None


def test_auth_token_only():
    event = construct_webhook_event(PAYLOAD, signed_headers(method_webhook_signature=None), auth_token=AUTH_TOKEN, now=NOW)
    assert event['payload']['op'] == 'update'


def test_rejects_tampered_and_reserialized_bodies():
    assert_code('invalid_signature', payload=PAYLOAD.replace('account.update', 'payment.update'),
                headers=signed_headers(), hmac_secret=HMAC_SECRET, now=NOW)
    assert_code('invalid_signature', payload=json.dumps(json.loads(PAYLOAD), indent=2),
                headers=signed_headers(), hmac_secret=HMAC_SECRET, now=NOW)


def test_rejects_wrong_secret_short_signature_and_swapped_timestamp():
    assert_code('invalid_signature', payload=PAYLOAD, headers=signed_headers(), hmac_secret='other', now=NOW)
    assert_code('invalid_signature', payload=PAYLOAD, headers=signed_headers(method_webhook_signature='abc'),
                hmac_secret=HMAC_SECRET, now=NOW)
    assert_code('invalid_signature', payload=PAYLOAD, headers=signed_headers(method_webhook_timestamp=str(NOW + 1)),
                hmac_secret=HMAC_SECRET, now=NOW)


def test_rejects_wrong_authorization():
    assert_code('invalid_authorization', payload=PAYLOAD,
                headers=signed_headers(authorization=base64.b64encode(b'nope').decode()), auth_token=AUTH_TOKEN, now=NOW)


def test_timestamp_tolerance():
    kwargs = dict(payload=PAYLOAD, headers=signed_headers(), hmac_secret=HMAC_SECRET)
    assert_code('timestamp_out_of_tolerance', now=NOW + 301, **kwargs)
    assert_code('timestamp_out_of_tolerance', now=NOW - 301, **kwargs)
    assert_code('timestamp_out_of_tolerance', now=NOW + 61, tolerance_seconds=60, **kwargs)
    assert construct_webhook_event(now=NOW + 300, **kwargs)['timestamp'] == NOW
    assert construct_webhook_event(now=NOW + 86400, tolerance_seconds=0, **kwargs)['timestamp'] == NOW


def test_missing_headers_and_secrets():
    assert_code('missing_secret', payload=PAYLOAD, headers=signed_headers(), now=NOW)
    assert_code('missing_header', payload=PAYLOAD, headers=signed_headers(method_webhook_timestamp=None), hmac_secret=HMAC_SECRET, now=NOW)
    assert_code('missing_header', payload=PAYLOAD, headers=signed_headers(method_webhook_signature=None), hmac_secret=HMAC_SECRET, now=NOW)
    assert_code('missing_header', payload=PAYLOAD, headers=signed_headers(authorization=None), auth_token=AUTH_TOKEN, now=NOW)


def test_bad_timestamp_and_non_json_body():
    assert_code('invalid_timestamp', payload=PAYLOAD, headers=signed_headers(method_webhook_timestamp='2024-10-01T00:00:00Z'),
                hmac_secret=HMAC_SECRET, now=NOW)
    for bad in ('\u00b2', '\u0661\u0662', '-5', '12.5', '1' * 5000):
        assert_code('invalid_timestamp', payload=PAYLOAD, headers=signed_headers(method_webhook_timestamp=bad),
                    hmac_secret=HMAC_SECRET, now=NOW)
    body = 'not json'
    assert_code('invalid_payload', payload=body, headers=signed_headers(method_webhook_signature=docs_signature(body, NOW, HMAC_SECRET)),
                hmac_secret=HMAC_SECRET, now=NOW)


def test_available_on_client_without_api_call():
    method = Method(env='dev', api_key='sk_test_offline')
    event = method.webhooks.construct_event(PAYLOAD, signed_headers(), hmac_secret=HMAC_SECRET, now=NOW)
    assert event['payload']['webhook_id'] == 'whk_cSGjA6d9N8y8R'


def test_error_is_a_value_error():
    with pytest.raises(ValueError):
        construct_webhook_event(PAYLOAD, signed_headers(), hmac_secret='other', now=NOW)
