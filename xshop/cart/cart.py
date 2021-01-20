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

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity.

        Args:
            product ([type]): [The product instance to add or update in the cart.]
            quantity (int, optional): [An optional integer with the product quantity, Defaults to 1.]
            override_quantity (bool, optional): [This is a Boolean that indicates whether the quantity
                        needs to be overridden with the given quantity ( True ), or whether the new
                        quantity has to be added to the existing quantity ( False ), Defaults to False.]
        """
        product_id = str(product["id"])
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": product["price"]}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
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
