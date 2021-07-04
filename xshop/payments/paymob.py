import requests
from typing import List, Dict
from django.conf import settings

base_url = "https://accept.paymob.com/api"


def token() -> str:
    url = f"{base_url}/auth/tokens"
    payload = {"api_key": settings.PAYMOB_API_KEY}
    resp = requests.post(url, json=payload)
    return resp.json().get("token")


def order(
    token: str, amount: int, merchant_order_id: str, items: List[Dict[str, str]]
) -> int:
    url = f"{base_url}/ecommerce/orders"
    payload = {
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": str(amount),
        "currency": "EGP",
        "merchant_order_id": merchant_order_id,
        "items": items,
        # Example items for now
        #  [
        #     {
        #         "name": "ASC1515",
        #         "amount_cents": "500000",
        #         "description": "Smart Watch",
        #         "quantity": "1",
        #     },
        #     {
        #         "name": "ERT6565",
        #         "amount_cents": "200000",
        #         "description": "Power Bank",
        #         "quantity": "1",
        #     },
        # ],
    }

    resp = requests.post(url, json=payload)
    return resp.json().get("id")


def key(
    token: str, amount: int, order_id: int, billing_data: dict, integration_id: int
):
    url = f"{base_url}/acceptance/payment_keys"
    payload = {
        "auth_token": token,
        "amount_cents": str(amount),
        "expiration": 3600,
        "order_id": str(order_id),
        "billing_data": billing_data,
        # {
        #     "apartment": "803",
        #     "email": "claudette09@exa.com",
        #     "floor": "42",
        #     "first_name": "Clifford",
        #     "street": "Ethan Land",
        #     "building": "8028",
        #     "phone_number": "+86(8)9135210487",
        #     "shipping_method": "PKG",
        #     "postal_code": "01898",
        #     "city": "Jaskolskiburgh",
        #     "country": "CR",
        #     "last_name": "Nicolas",
        #     "state": "Utah"
        # },
        "currency": "EGP",
        "integration_id": integration_id,
        "lock_order_when_paid": "false",
    }

    resp = requests.post(url, json=payload)
    return resp.json().get("token")


def issue_payment() -> str:
    # auth
    # order
    # key

    # iframe
    return
