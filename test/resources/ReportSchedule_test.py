import os
from method import Method
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

report_schedule_create_response = None
report_schedule_list_response = None
report_schedule_retrieve_response = None
report_schedule_update_response = None


def test_create_report_schedule():
    global report_schedule_create_response

    report_schedule_create_response = method.report_schedules.create({
        'types': ['ach.pull.nightly'],
        'delivery_methods': ['webhook', 'email'],
        'recipients': ['example@methodfi.com'],
        'cron': '0 8 * * *',
    })

    expect_results = {
        "id": report_schedule_create_response["id"],
        "types": ["ach.pull.nightly"],
        "delivery_methods": ["webhook", "email"],
        "recipients": ["example@methodfi.com"],
        "cron": "0 8 * * *",
        "status": "active",
        "created_at": report_schedule_create_response["created_at"],
        "updated_at": report_schedule_create_response["updated_at"],
    }

    assert report_schedule_create_response == expect_results


def test_list_report_schedules():
    global report_schedule_list_response

    report_schedule_list_response = method.report_schedules.list()

    ids = [schedule['id'] for schedule in report_schedule_list_response]
    assert report_schedule_create_response['id'] in ids


def test_retrieve_report_schedule():
    global report_schedule_retrieve_response

    report_schedule_retrieve_response = method.report_schedules.retrieve(report_schedule_create_response['id'])

    expect_results = {
        "id": report_schedule_create_response["id"],
        "types": ["ach.pull.nightly"],
        "delivery_methods": ["webhook", "email"],
        "recipients": ["example@methodfi.com"],
        "cron": "0 8 * * *",
        "status": "active",
        "created_at": report_schedule_retrieve_response["created_at"],
        "updated_at": report_schedule_retrieve_response["updated_at"],
    }

    assert report_schedule_retrieve_response == expect_results


def test_add_report_schedule_type():
    response = method.report_schedules(report_schedule_create_response['id']).types.add({
        'type': 'payments.created.previous',
    })

    assert 'payments.created.previous' in response['types']


def test_replace_report_schedule_types():
    response = method.report_schedules(report_schedule_create_response['id']).types.replace({
        'types': ['ach.pull.nightly', 'payments.failed.previous_day'],
    })

    assert response['types'] == ['ach.pull.nightly', 'payments.failed.previous_day']


def test_remove_report_schedule_type():
    response = method.report_schedules(report_schedule_create_response['id']).types.delete('payments.failed.previous_day')

    assert 'payments.failed.previous_day' not in response['types']


def test_add_report_schedule_delivery_method():
    response = method.report_schedules(report_schedule_create_response['id']).delivery_methods.add({
        'delivery_method': 'email',
    })

    assert 'email' in response['delivery_methods']


def test_replace_report_schedule_delivery_methods():
    response = method.report_schedules(report_schedule_create_response['id']).delivery_methods.replace({
        'delivery_methods': ['webhook'],
    })

    assert response['delivery_methods'] == ['webhook']


def test_remove_report_schedule_delivery_method():
    method.report_schedules(report_schedule_create_response['id']).delivery_methods.add({
        'delivery_method': 'email',
    })

    response = method.report_schedules(report_schedule_create_response['id']).delivery_methods.delete('email')

    assert 'email' not in response['delivery_methods']


def test_add_report_schedule_recipient():
    response = method.report_schedules(report_schedule_create_response['id']).recipients.add({
        'recipient': 'reports@methodfi.com',
    })

    assert 'reports@methodfi.com' in response['recipients']


def test_replace_report_schedule_recipients():
    response = method.report_schedules(report_schedule_create_response['id']).recipients.replace({
        'recipients': ['ops@methodfi.com'],
    })

    assert response['recipients'] == ['ops@methodfi.com']


def test_remove_report_schedule_recipient():
    method.report_schedules(report_schedule_create_response['id']).recipients.add({
        'recipient': 'temp@methodfi.com',
    })

    response = method.report_schedules(report_schedule_create_response['id']).recipients.delete('temp@methodfi.com')

    assert 'temp@methodfi.com' not in response['recipients']


def test_update_report_schedule():
    global report_schedule_update_response

    report_schedule_update_response = method.report_schedules.update(report_schedule_create_response['id'], {
        'cron': '0 9 * * 1-5',
    })

    assert report_schedule_update_response['cron'] == '0 9 * * 1-5'


def test_delete_report_schedule():
    report_schedule_delete_response = method.report_schedules.delete(report_schedule_create_response['id'])

    assert report_schedule_delete_response == None
