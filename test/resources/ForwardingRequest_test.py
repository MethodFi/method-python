import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

pytestmark = pytest.mark.skipif(not API_KEY, reason='API_KEY is not set; skipping live dev API tests.')

method = Method(env='dev', api_key=API_KEY)

# Forwarding requests are executed synchronously against a destination URL that must be
# whitelisted for the team (e.g. Fidel, Tabapay, Recurly), and their bindings must reference
# real resources owned by the team (e.g. a card payment instrument, a secret, an entity).
# A maintainer must provide the following to exercise these tests, then remove the skips:
#   FWD_REQUEST_URL         - a destination URL whitelisted for the team
#   FWD_REQUEST_PMT_INST_ID - an active card payment instrument id (pmt_inst_...) owned by the team
FWD_REQUEST_URL = os.getenv('FWD_REQUEST_URL')
FWD_REQUEST_PMT_INST_ID = os.getenv('FWD_REQUEST_PMT_INST_ID')

SKIP_REASON = (
    'Requires a whitelisted destination URL (FWD_REQUEST_URL) and a real card payment '
    'instrument (FWD_REQUEST_PMT_INST_ID) provisioned for the team in the dev environment.'
)

forwarding_requests_create_response = None
forwarding_requests_retrieve_response = None

@pytest.fixture(scope='module')
def setup():
    holder_1_response = method.entities.create({
        'type': 'individual',
        'individual': {
            'first_name': 'Kevin',
            'last_name': 'Doyle',
            'dob': '1930-03-11',
            'email': 'kevin.doyle@gmail.com',
            'phone': '+15121231111',
        }
    })

    secret_1_response = method.secrets.create({
        'value': 'test_secret_value'
    })

    yield {
        'holder_1_id': holder_1_response['id'],
        'secret_1_id': secret_1_response['id'],
    }

    # Entities cannot be deleted via the public API, so only the secret is cleaned up.
    method.secrets.delete(secret_1_response['id'])


@pytest.mark.skip(reason=SKIP_REASON)
def test_create_forwarding_request(setup):
    global forwarding_requests_create_response

    forwarding_requests_create_response = method.forwarding_requests.create({
        'bindings': {
            'card': FWD_REQUEST_PMT_INST_ID,
            'individual': setup['holder_1_id'],
            'api_key': setup['secret_1_id'],
        },
        'url': FWD_REQUEST_URL,
        'method': 'POST',
        'headers': {
            'Authorization': 'Bearer {{ api_key.value }}'
        },
        'body': '{ "card": { "accountNumber": "{{ card.number }}" }, "owner": { "firstName": "{{ individual.first_name }}", "lastName": "{{ individual.last_name }}" } }'
    })

    expect_results = {
        'id': forwarding_requests_create_response['id'],
        'bindings': {
            'card': FWD_REQUEST_PMT_INST_ID,
            'individual': setup['holder_1_id'],
            'api_key': setup['secret_1_id'],
        },
        'request': forwarding_requests_create_response['request'],
        'response': forwarding_requests_create_response['response'],
        'duration_ms': forwarding_requests_create_response['duration_ms'],
        'status': 'completed',
        'status_history': forwarding_requests_create_response['status_history'],
        'created_at': forwarding_requests_create_response['created_at'],
    }

    assert forwarding_requests_create_response == expect_results


@pytest.mark.skip(reason=SKIP_REASON)
def test_retrieve_forwarding_request(setup):
    global forwarding_requests_retrieve_response

    forwarding_requests_retrieve_response = method.forwarding_requests.retrieve(forwarding_requests_create_response['id'])

    expect_results = {
        'id': forwarding_requests_create_response['id'],
        'bindings': forwarding_requests_create_response['bindings'],
        'request': forwarding_requests_retrieve_response['request'],
        'response': forwarding_requests_retrieve_response['response'],
        'duration_ms': forwarding_requests_retrieve_response['duration_ms'],
        'status': forwarding_requests_retrieve_response['status'],
        'status_history': forwarding_requests_retrieve_response['status_history'],
        'created_at': forwarding_requests_retrieve_response['created_at'],
    }

    assert forwarding_requests_retrieve_response == expect_results
