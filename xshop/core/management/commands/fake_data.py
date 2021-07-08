import random
from django.core.management.base import BaseCommand
from djmoney.money import Money

import factory
from factory import fuzzy
from factory.faker import Faker

from xshop.shops.models import Shop
from xshop.products.models import Product

# from xshop.orders.models import Order
# from xshop.invoices.models import Invoice


# Factories
class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    mobile = f"01010092{random.randint(100,999)}"
    name = Faker("name")
    description = Faker("sentence")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker("name")
    price = fuzzy.FuzzyDecimal(1, 999)
    stock = fuzzy.FuzzyInteger(0, 1000)
    description = Faker("sentence")


class Command(BaseCommand):
    def handle(self, *args, **options):
        # =========== Groups
        # re-use the previously made commands here

        # =========== Permissions
        # re-use the previously made commands here

        # =========== Users
        # Customers
        # Cashiers
        # DECs
        # General Managers

        # =========== Shops
        # create multiple shops
        self.stdout.write(">> Creating Shops...")
        shops = ShopFactory.create_batch(10)
        self.stdout.write("Done.")

        # =========== Products
        # create 20 products for each shop
        self.stdout.write(">> Creating Products...")
        for shop in shops:
            ProductFactory.create_batch(20, shop=shop)
        self.stdout.write("Done.")

        # =========== Orders
        # Create multiple orders for multiple users with random products made above

        # =========== PaymentAttempts TODO after payments merge

        # =========== Invoices
        # Create multiple invoices related to users who have made orders
