from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from xshop.cart.cart import Cart

# from xshop.payments import paymob


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
        super().save(*args, **kwargs)

    def after(self, request):
        # NOTE Keep it dummy no need for too much validations, it's a GP anyway :3
        # make sure of transaction status from paymob
        # transaction_id = request_data.get("id")
        # transaction = paymob.retrieve_transaction(transaction_id)
        # # make sure same transaction
        # assert transaction.get("merchant_order_id") == self.mutual_reference

        request_data = request.GET

        # update payment attempt
        pending = request_data.get("pending")
        success = request_data.get("success")

        if pending == "false":
            if success == "true":
                self.status = "Successful"
            elif success == "false":
                self.status = "Failed"
        self.gateway_transaction_id = request_data.get("id")

        # commit db
        self.save()

        # mark order paid if successful attempt
        if self.status == "Successful":
            self.order.paid = True
            self.order.save()

        # clear cart after success
        cart = Cart(request)
        cart.clear()
