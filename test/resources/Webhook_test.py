import os
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

webhooks_create_response = None
webhooks_retrieve_response = None
webhooks_list_response = None
webhooks_delete_response = None

def test_create_webhooks():
    global webhooks_create_response

    webhooks_create_response = method.webhooks.create({
        'type': 'payment.create',
        'url': 'https://dev.methodfi.com',
        'auth_token': 'test_auth_token'
    })

    expect_results = {
        'id': webhooks_create_response['id'],
        'type': 'payment.create',
        'url': 'https://dev.methodfi.com',
        'metadata': None,
        'created_at': webhooks_create_response['created_at'],
        'updated_at': webhooks_create_response['updated_at'],
        'expand_event': webhooks_create_response['expand_event'],
        'status': webhooks_create_response['status'],
        'error': webhooks_create_response['error']
    }

    assert webhooks_create_response == expect_results


def test_retrieve_webhook():
    global webhooks_retrieve_response

    webhooks_retrieve_response = method.webhooks.retrieve(webhooks_create_response['id'])

    expect_results = {
        'id': webhooks_create_response['id'],
        'type': 'payment.create',
        'url': 'https://dev.methodfi.com',
        'metadata': None,
        'created_at': webhooks_retrieve_response['created_at'],
        'updated_at': webhooks_retrieve_response['updated_at'],
        'expand_event': webhooks_retrieve_response['expand_event']
    }

    assert webhooks_retrieve_response == expect_results


def test_list_webhooks():
    global webhooks_list_response

    webhooks_list_response = method.webhooks.list()
    webhook_ids = [webhook['id'] for webhook in webhooks_list_response]

    assert webhooks_create_response['id'] in webhook_ids


def test_delete_webhook():
    global webhooks_delete_response

    webhooks_delete_response = method.webhooks.delete(webhooks_create_response['id'])

    assert webhooks_delete_response == None
