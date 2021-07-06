from django.core.validators import MinValueValidator
from django.db import models
from model_utils.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


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

    @property
    def total_price(self):
        return sum(item.total_price for item in self.order_item_set.iterator())


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

    def clean(self, *args, **kwargs):
        if self.order.paid:
            raise ValidationError(_("You can not add order items to paid orders"))

        if self.quantity > self.product.stock:
            raise ValidationError(
                _(
                    "Max quantity for {} is {}".format(
                        self.product.name, self.product.stock
                    )
                )
            )
        super(OrderItem, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(OrderItem, self).save(*args, **kwargs)
