from django.core.management.base import BaseCommand

from xshop.shops.models import Shop
from xshop.products.models import Product
from xshop.orders.models import Order
from xshop.invoices.models import Invoice


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(">> Removing all shops...")
        Shop.objects.all().delete()
        self.stdout.write("Done.")

        self.stdout.write(">> Removing all products...")
        Product.objects.all().delete()
        self.stdout.write("Done.")

        self.stdout.write(">> Removing all orders...")
        Order.objects.all().delete()
        self.stdout.write("Done.")

        self.stdout.write(">> Removing all invoices...")
        Invoice.objects.all().delete()
        self.stdout.write("Done.")
