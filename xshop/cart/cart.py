from django.conf import settings
from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer


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
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 1, "price": product["price"]}
        self.save()

    def update(self, product, quantity):
        """
        update product quantity
        """
        product_id = str(product["id"])
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product_id):
        """
        Remove a product from the cart.
        """
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            serialized_product = ProductSerializer(product)
            cart[str(product.id)]["product"] = serialized_product.data

        for item in cart.values():
            item["total_price"] = float(item["price"]) * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Return total price for all products in cart.
        """
        return sum(
            float(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
