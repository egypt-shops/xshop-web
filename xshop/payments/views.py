from django.http.response import HttpResponseBadRequest
from xshop.payments import paymob
from django.shortcuts import render
from pprint import pprint


def get_transaction_status(transaction: dict) -> str:
    pending = transaction.get("pending")
    success = transaction.get("success")

    if pending is False and success is True:
        return "Successful"
    elif pending is False and success is False:
        return "Failed"
    elif pending is True and success is False:
        return "Pending"
    else:
        return "Unknown"


def redirect(request):
    data = request.GET

    pprint(data)
    breakpoint()

    # get useful data from parameters
    transaction_id = data.get("obj").get("id")

    # handle transaction objects only
    if not data or not transaction_id or data.get("type") != "TRANSACTION":
        return HttpResponseBadRequest()

    # make sure of transaction status from paymob
    transaction = paymob.retrieve_transaction(transaction_id)

    status = get_transaction_status(transaction)

    ## TODO
    # common_reference = order.get("merchant_order_id")

    # save status locally

    # present result to the user

    return render(request, "Return Redirect")
