from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from model_utils.models import TimeStampedModel


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default=Money(0, "EGP"))
    stock = models.PositiveIntegerField()
    # TODO add later
    # barcode
    # qr_code
    added_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
