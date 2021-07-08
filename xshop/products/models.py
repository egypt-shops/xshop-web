from io import BytesIO

import barcode
from django.core.validators import MinValueValidator, MaxValueValidator
from barcode.writer import ImageWriter
from django.core.files import File
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from model_utils.models import TimeStampedModel
from xshop.users.models import User


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    price = MoneyField(max_digits=14, decimal_places=2, default=Money(0, "EGP"))
    stock = models.PositiveIntegerField()
    barcode = models.ImageField(upload_to="images/", blank=True, null=True)
    country_id = models.CharField(max_length=1, null=True, blank=True)
    manufacturer_id = models.CharField(max_length=6, null=True, blank=True)
    number_id = models.CharField(max_length=5, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    picture = models.ImageField(upload_to="images/products/", default="no_picture.png")

    # TODO add later
    # qr_code
    added_by = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        code39 = barcode.get_barcode_class("code39")
        ean = code39(
            f"{self.country_id}{self.manufacturer_id}{self.number_id}",
            writer=ImageWriter(),
        )
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save("barcode.png", File(buffer), save=False)
        return super().save(*args, **kwargs)


class Rating(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.PROTECT)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
