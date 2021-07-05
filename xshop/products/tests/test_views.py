from django.test import Client, TestCase, tag
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from xshop.products.models import Product
from xshop.users.models import User


@tag("productdetailview")
class ProductDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010101010",
            name="Hatem",
        )
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.product = baker.make(Product, stock=10, price=10)
        self.client = Client()
        self.url = reverse(
            "product:product_details", kwargs={"product_id": self.product.id}
        )

    def test_get_product_details_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertRedirects(
            resp,
            "/users/login/?next=/product/{}/".format(self.product.id),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_get_product_details(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "pages/product_detail.html")

    def test_retreive_product_details(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get("/product/{}/".format(self.product.id))
        self.assertEqual(resp.context["price"], str(self.product.price)[4:])
        self.assertEqual(resp.context["product"], self.product)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
