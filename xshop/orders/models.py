from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel


class Order(TimeStampedModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.SET_NULL, null=True, blank=True
    )
    paid = models.BooleanField(default=False)

    @property
    def get_data(self):
        return dict(zip(["shop_pk", "user_pk"], [self.shop.pk, self.user.pk]))


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)], default=1)

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity
