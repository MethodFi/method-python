import os
from method import Method
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv('API_KEY')

method = Method(env='dev', api_key=API_KEY)

card_product_retrieve_response = None


def test_retrieve_card_product():
    global card_product_retrieve_response

    card_product_retrieve_response = method.card_products.retrieve('pdt_15')

    expect_results = {
        "id": "pdt_17",
        "name": "Chase Freedom",
        "issuer": "Chase",
        "type": "specific",
        "brands": [
          {
              "id": "pdt_17_brd_1",
              "description": "Chase Freedom",
              "network": "visa",
              "default_image": "https://static.methodfi.com/card_brands/fb5fbd6a5d45b942752b9dc641b93d1f.png"
          },
          {
              "id": "pdt_17_brd_2",
              "description": "Chase Freedom",
              "network": "visa",
              "default_image": "https://static.methodfi.com/card_brands/6cb697528b0771f982f7c0e8b8869de3.png"
          }
        ],
        "error": None,
        "created_at": card_product_retrieve_response['created_at'],
        "updated_at": card_product_retrieve_response['updated_at'],
      }

    assert card_product_retrieve_response == expect_results