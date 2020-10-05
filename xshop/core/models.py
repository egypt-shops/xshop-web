from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField
from djmoney.money import Money
from djmoney.models.fields import MoneyField


class Shop(TimeStampedModel):
    mobile = PhoneNumberField()
    name = models.CharField(max_length=255)
    dashboard_modules = MultiSelectField(choices=settings.DASHBOARD_MODULES, blank=True)


class PricingPlan(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default=Money(0, "EGP"))
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)


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
