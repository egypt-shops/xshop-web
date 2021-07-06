from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from xshop.payments import paymob


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


class PaymentAttempt(TimeStampedModel):
    # The mutual reference between us and the payment gateway (merchant_order_id in paymob)
    mutual_reference = models.CharField(
        max_length=36, blank=True, null=True, editable=False
    )
    gateway_transaction_id = models.CharField(
        max_length=36, blank=True, null=True, editable=False
    )
    status = models.CharField(max_length=12, blank=True, null=True, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.PROTECT, editable=False)

    def clean(self):
        if self.order.paid:
            raise ValidationError("Payment can not be issued for a paid order")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(self, *args, **kwargs)

    def after(self, request_data: dict):
        # make sure of transaction status from paymob
        transaction_id = request_data.get("id")
        transaction = paymob.retrieve_transaction(transaction_id)

        # make sure same transaction
        assert (
            transaction.get("order").get("merchant_order_id") == self.mutual_reference
        )

        # update payment attempt
        self.status = get_transaction_status(transaction)
        self.gateway_transaction_id = transaction_id

        # commit db
        self.save()

        # mark order paid if successful attempt
        if self.status == "Successful":
            self.order.paid = True
            self.order.save()
