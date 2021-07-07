from django.conf import settings
from django.core.exceptions import ValidationError

from xshop.products.models import Product
from xshop.cart.api.serializers import ProdcutCartSerializer


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product):
        """Add a product to the cart or update its quantity.

        Args:
            product ([object]): [The product instance to add or update in the cart.]
        """
        product_id = str(product["id"])
        shop = str(product["shop"])
        if shop not in self.cart:
            self.cart[shop] = {}
        if product_id not in self.cart[shop].keys():
            self.cart[shop][product_id] = {"quantity": 1, "price": product["price"]}
        self.save()

    def update(self, product, quantity):
        """
        update product quantity
        """
        product_id = str(product["id"])
        shop = str(product["shop"])
        if shop in self.cart and str(product_id) in self.cart[shop]:
            self.cart[shop][product_id]["quantity"] = quantity
        else:
            raise ValidationError({"error": "shop or product not found"})
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product["id"])
        shop = str(product["shop"])
        if shop in self.cart and product_id in self.cart[shop]:
            del self.cart[shop][product_id]
            if not self.cart[shop]:
                del self.cart[shop]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        # get last element added only
        if list(self.cart.keys()):
            shop_id = list(self.cart.keys())[-1]
            product_ids = self.cart[shop_id].keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)

            cart = self.cart.copy()
            for product in products:
                serialized_product = ProdcutCartSerializer(product)
                cart[shop_id][str(product.id)]["product"] = serialized_product.data

            for item in cart[shop_id].values():
                item["total_price"] = float(item["price"]) * item["quantity"]
                yield item

    def __len__(self) -> int:
        """
        Count all items in the cart.
        """
        shop_id = list(self.cart.keys())[-1]
        return sum(item["quantity"] for item in self.cart[shop_id].values())

    def get_total_price(self) -> float:
        """
        Return total price for all products in cart.
        """
        shop_id = list(self.cart.keys())[-1]
        return sum(
            float(item["price"]) * item["quantity"]
            for item in self.cart[shop_id].values()
        )

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
