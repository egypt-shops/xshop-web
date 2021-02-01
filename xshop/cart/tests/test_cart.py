from django.contrib.auth import get_user_model
from django.test import tag
from model_bakery import baker
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer
from xshop.cart.cart import Cart

User = get_user_model()


@tag("cart")
class TestCart(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User, mobile="01010101010", name="Test User")
        self.product = baker.make(Product, stock=10, price=12)

        self.factory = RequestFactory()

    def test_init_cart(self):
        request = self.factory.get("/")
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["modified"] = False
        request.session.save()
        Cart(request)

        self.assertIn("cart", request.session)
        self.assertFalse(request.session["modified"])

    def test_add_product_to_cart(self):
        request = self.factory.get("/")
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["modified"] = False
        cart = Cart(request)
        cart.add(ProductSerializer(self.product).data)

        self.assertIn("cart", request.session)
        self.assertTrue(request.session.modified)
        self.assertFalse(request.session.is_empty())
        self.assertEqual(len(request.session["cart"]), 1)
        self.assertEqual(
            request.session["cart"].get(str(self.product.id))["quantity"], 1
        )

    def test_update_product_in_cart(self):
        request = self.factory.get("/")
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["modified"] = False
        cart = Cart(request)
        cart.add(ProductSerializer(self.product).data)
        cart.update(ProductSerializer(self.product).data, 3)

        self.assertIn("cart", request.session)
        self.assertTrue(request.session.modified)
        self.assertFalse(request.session.is_empty())
        self.assertEqual(len(request.session["cart"]), 1)
        self.assertEqual(
            request.session["cart"].get(str(self.product.id))["quantity"], 3
        )

    def test_remove_product_from_cart(self):
        request = self.factory.get("/")
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["modified"] = False
        cart = Cart(request)
        cart.add(ProductSerializer(self.product).data)
        cart.remove(self.product.id)

        self.assertIn("cart", request.session)
        self.assertTrue(request.session.modified)
        self.assertEqual(len(request.session["cart"]), 0)

    def test_clear_cart(self):
        request = self.factory.get("/")
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session["modified"] = False
        request.session.save()
        Cart(request).clear()

        self.assertNotIn("cart", request.session)
