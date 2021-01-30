from django.contrib.auth import get_user_model
from django.test import tag
from model_bakery import baker
from django.test import TestCase, RequestFactory

from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer
from xshop.cart.cart import Cart

User = get_user_model()


@tag("cart")
class TestCart(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010101010", name="Test User")
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.product = baker.make(Product, stock=10)

        self.request = RequestFactory()
        self.request.user = self.user

    def test_add_to_cart(self):
        Cart.add(product=ProductSerializer(self.product).data)

        self.assertIn("cart", self.session)

    # def test_update_product_in_cart(self):
    #     pass

    # def test_remove_product_from_cart(self):
    #     pass

    # def clear_cart(self):
    #     pass
