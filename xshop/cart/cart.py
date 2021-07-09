# from inspect import currentframe
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

        # Cart
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            # Save a None current_shop fieald in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

        # Shop
        if not self.session.get(settings.CURRENT_SHOP_SESSION_ID):
            self.session[settings.CURRENT_SHOP_SESSION_ID] = None

    def add(self, product):
        """Add a product to the cart or update its quantity.

        Args:
            product ([object]): [The product instance to add or update in the cart.]
        """
        product_id = str(product["id"])
        shop = str(product["shop"])
        self.session["current_shop"] = shop
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
            self.session["current_shop"] = shop
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
            self.session["current_shop"] = shop
            if not self.cart[shop]:
                del self.cart[shop]
                if self.cart:
                    self.session["current_shop"] = list(self.cart.keys())[-1]
                else:
                    self.session["current_shop"] = None
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        # get last element added only
        if not list(self.cart.keys()):
            return {}
        shop_id = self.session["current_shop"]
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
        if list(self.cart.keys()):
            shop_id = self.session["current_shop"]
            return sum(item["quantity"] for item in self.cart[shop_id].values())
        else:
            return 0

    def get_total_price(self) -> float:
        """
        Return total price for all products in cart.
        """
        if list(self.cart.keys()):
            shop_id = self.session["current_shop"]
            return sum(
                float(item["price"]) * item["quantity"]
                for item in self.cart[shop_id].values()
            )
        else:
            return 0

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
