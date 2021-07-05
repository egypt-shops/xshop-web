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

    trx = data.get("obj")

    # handle transaction objects only
    if not data or not trx or data.get("type") != "TRANSACTION":
        return

    # extract useful data from the transaction
    paymob_trx_id = trx.get("id")
    trx_status = get_transaction_status(trx)
    order = trx.get("order")
    paymob_order_id = order.get("id")
    common_reference = order.get("merchant_order_id")
    # make sure of transaction status

    # save status locally

    # present result to the user

    return render(request, "Return Redirect")
