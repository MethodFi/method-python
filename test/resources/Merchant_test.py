import os
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

merchant_retrieve_response = None
merchants_list_response = None
amex_mch_id = 'mch_3'
amex_provider_id_plaid = 'ins_10'


def test_retrieve_merchant():
    global merchant_retrieve_response

    merchant_retrieve_response = method.merchants.retrieve(amex_mch_id)

    assert merchant_retrieve_response['id'] == 'mch_3'
    assert merchant_retrieve_response['parent_name'] == 'American Express'
    assert merchant_retrieve_response['type'] == 'credit_card'
    assert merchant_retrieve_response['provider_ids']['plaid'] == ['ins_10']
    assert merchant_retrieve_response['provider_ids']['mx'] == ['amex']
    assert merchant_retrieve_response['is_temp'] is False


def test_list_merchants():
    global merchants_list_response

    merchants_list_response = method.merchants.list({ 'provider_id.plaid': amex_provider_id_plaid })
    merchant_to_use = merchants_list_response[0]

    assert merchants_list_response != None
    assert isinstance(merchants_list_response._data, list)
    assert merchant_to_use['parent_name'] == 'American Express'
    assert merchant_to_use['type'] == 'credit_card'
    assert merchant_to_use['provider_ids']['plaid'] == ['ins_10']
    assert merchant_to_use['provider_ids']['mx'] == ['amex']
    assert merchant_to_use['is_temp'] is False
