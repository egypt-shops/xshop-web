from django.shortcuts import get_object_or_404, render

from xshop.payments.models import PaymentAttempt


def result(request):
    """Post Payment (Redirect Response from PayMob)"""
    data = request.GET

    # # Cash On Delivery

    if data.get("paying_method") == "CASH_ON_DELIVERY":
        return render(
            request,
            "payments/result.dt.html",
            {
                "order_id": data.get("order_id"),
                "paying_method": data.get("paying_method"),
            },
        )

    # # Credit Card

    mutual_reference = data.get("merchant_order_id")
    payment_attempt = get_object_or_404(
        PaymentAttempt, mutual_reference=mutual_reference
    )
    payment_attempt.after(data)

    return render(
        request,
        "payments/result.dt.html",
        {
            "status": payment_attempt.status,
            "mutual_reference": mutual_reference,
            "order_id": payment_attempt.order.id,
            "paying_method": "CREDIT_CARD",
        },
    )
