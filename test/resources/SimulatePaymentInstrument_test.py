import os
import pytest
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

pytestmark = pytest.mark.skipif(not API_KEY, reason='API_KEY is not set; skipping live dev API tests.')

method = Method(env='dev', api_key=API_KEY)

SIMULATE_PAYMENT_INSTRUMENT_SKIP_REASON = (
    'POST /simulate/payments/payment_instruments/:pmt_inst_id requires an account with an active '
    'inbound_achwire_payment payment instrument; the shared dev environment provides no such fixture.'
)


@pytest.mark.skip(reason=SIMULATE_PAYMENT_INSTRUMENT_SKIP_REASON)
def test_simulate_payment_via_payment_instrument():
    pmt_inst_id = os.getenv('INBOUND_ACHWIRE_PAYMENT_INSTRUMENT_ID')

    simulate_payment_response = method.simulate.payments.payment_instruments(pmt_inst_id).create({
        'amount': 5000,
        'ach_reference_id': 'TESTREF123',
        'description': 'MethodPy',
    })

    assert simulate_payment_response['id'] is not None
    assert simulate_payment_response['amount'] == 5000
