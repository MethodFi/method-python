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

    expect_results = {
        "id": "mch_3",
        "parent_name": "American Express",
        "name": "American Express - Credit Cards",
        "logo": "https://static.methodfi.com/mch_logos/mch_3.png",
        "type": "credit_card",
        "provider_ids": {
            "plaid": ["ins_10"],
            "mx": ["amex"],
            "finicity": [],
            "dpp": ["120", "18954427", "11859365", "18947131", "16255844"]
        },
        "is_temp": False,
        "account_number_formats": []
    }

    assert merchant_retrieve_response == expect_results


def test_list_merchants():
    global merchants_list_response

    merchants_list_response = method.merchants.list({ 'provider_id.plaid': amex_provider_id_plaid })
    merchant_to_use = merchants_list_response[0]

    expect_results = {
        "id": "mch_300485",
        "parent_name": "American Express",
        "name": "American Express Credit Card",
        "logo": "https://static.methodfi.com/mch_logos/mch_300485.png",
        "type": "credit_card",
        "provider_ids": {
            "plaid": ["ins_10"],
            "mx": ["amex"],
            "finicity": [],
            "dpp": [
                '7929257',
                '120',
                '18391555',
                '18954427',
                '11859365',
                '18947131',
                '16255844'
            ]
        },
        "is_temp": False,
        "account_number_formats": [
            '###############'
        ]
    }

    assert merchants_list_response != None
    assert isinstance(merchants_list_response._data, list)
    assert merchant_to_use == expect_results
