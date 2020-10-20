from django.db import models
from model_utils.models import TimeStampedModel


class Invoice(TimeStampedModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Cashier or Customer",
        null=True,
        blank=True,
    )
    order = models.ForeignKey("orders.Order", on_delete=models.PROTECT)
