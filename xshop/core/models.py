from django.core.validators import MinValueValidator
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

    def __str__(self):
        return self.name


class PricingPlan(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default=Money(0, "EGP"))
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False)


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)], default=1)

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Invoice(TimeStampedModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Cashier or Customer",
        null=True,
        blank=True,
    )
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
