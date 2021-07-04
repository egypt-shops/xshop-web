from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField


class Shop(TimeStampedModel):
    mobile = PhoneNumberField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)
    picture = models.ImageField(upload_to="images/shops/", default="no_picture.png")
    dashboard_modules = MultiSelectField(choices=settings.DASHBOARD_MODULES, blank=True)

    def __str__(self):
        return self.name


class PricingPlan(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default=Money(0, "EGP"))
    shop = models.OneToOneField(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
