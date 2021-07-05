from django.shortcuts import render
from django.http import JsonResponse
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


# NOTE this might not be useful at all... think about leaving it.
def callback(request):
    data = request.POST
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

    # get local payment attempt

    # Update payment status in db

    # if success mark order paid and empty user cart for current shop

    # else: leave cart as is, notiffy the user to go back and try again
    return JsonResponse()


def redirect(request):
    data = request.GET

    pprint(data)

    # get useful data from parameters

    # make sure of transaction status

    # save status locally

    # present result to the user

    return render()
