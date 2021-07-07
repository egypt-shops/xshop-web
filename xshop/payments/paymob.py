import requests
from dataclasses import dataclass
from typing import List
from django.conf import settings

base_url = "https://accept.paymob.com/api"


def token() -> str:
    url = f"{base_url}/auth/tokens"
    payload = {"api_key": getattr(settings, "PAYMOB_API_KEY")}
    resp = requests.post(url, json=payload)
    return resp.json().get("token")


@dataclass
class OrderItem:
    name: str
    amount_cents: str
    description: str
    quantity: str


def order(
    token: str, amount: int, merchant_order_id: str, items: List[OrderItem]
) -> int:
    url = f"{base_url}/ecommerce/orders"
    payload = {
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": str(amount),
        "currency": "EGP",
        "merchant_order_id": merchant_order_id,
        "items": items,
    }

    resp = requests.post(url, json=payload)
    return resp.json().get("id")


@dataclass
class BillingData:
    apartment: str
    email: str
    floor: str
    first_name: str
    street: str
    building: str
    phone_number: str
    shipping_method: str
    postal_code: str
    city: str
    country: str
    last_name: str
    state: str


def key(
    token: str,
    amount: int,
    order_id: int,
    billing_data: BillingData,
):
    url = f"{base_url}/acceptance/payment_keys"
    integration_id = getattr(settings, "PAYMOB_CARD_INTEGRATION_ID")
    payload = {
        "auth_token": token,
        "amount_cents": str(amount),
        "expiration": 3600,
        "order_id": str(order_id),
        "billing_data": billing_data,
        "currency": "EGP",
        "integration_id": integration_id,
        "lock_order_when_paid": "false",
    }

    resp = requests.post(url, json=payload)
    return resp.json().get("token")


def iframe_url(payment_key: str) -> str:
    iframe_id = getattr(settings, "PAYMOB_IFRAME_ID")
    return f"https://accept.paymob.com/api/acceptance/iframes/{iframe_id}?payment_token={payment_key}"


def issue_payment(
    amount: int,
    merchant_order_id: str,
    items: List[OrderItem],
    billing_data: BillingData,
) -> str:
    # auth
    auth_token = token()
    # order
    order_id = order(auth_token, amount, merchant_order_id, items)
    # key
    payment_key = key(auth_token, amount, order_id, billing_data)
    # iframe
    return iframe_url(payment_key)


def retrieve_transaction(transaction_id: str):
    auth_token = token()

    url = f"{base_url}/acceptance/transactions/{transaction_id}​"
    resp = requests.get(url, headers={"Authorization": f"Bearer {auth_token}"})

    # Transaction object
    return resp.json().get("obj")
