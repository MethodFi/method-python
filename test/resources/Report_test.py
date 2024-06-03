import os
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

report_create_response = None
report_retrieve_response = None
report_download_response = None


def test_create_report():
    global report_create_response

    report_create_response = method.reports.create({
        'type': 'payments.created.current',
    })

    expect_results = {
        "id": report_create_response["id"],
        "type": "payments.created.current",
        "url": f"https://dev.methodfi.com/reports/{report_create_response['id']}/download",
        "status": "completed",
        "metadata": None,
        "created_at": report_create_response["created_at"],
        "updated_at": report_create_response["updated_at"],
    }

    assert report_create_response == expect_results


def test_retrieve_report():
    global report_retrieve_response

    report_retrieve_response = method.reports.retrieve(report_create_response['id'])

    expect_results = {
        "id": report_create_response["id"],
        "type": "payments.created.current",
        "url": f"https://dev.methodfi.com/reports/{report_create_response['id']}/download",
        "status": "completed",
        "metadata": None,
        "created_at": report_retrieve_response["created_at"],
        "updated_at": report_retrieve_response["updated_at"],
    }

    assert report_retrieve_response == expect_results


def test_download_report():
    global report_download_response

    report_download_response = method.reports.download(report_create_response['id'])

    assert report_download_response is not None
