from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from xshop.invoices.models import Invoice
from xshop.orders.models import Order
from xshop.shops.models import Shop
from xshop.users.models import User


class InvoiceApiTests(APITestCase):
    def detail_patch_url(self, invoice_id):
        return reverse("invoices_api:invoice_detail_patch", args=[invoice_id])

    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01011698551",
            name="Ziad Mohamed Nabil",
        )
        self.user.set_password("test")
        self.user.save()
        self.shop1 = baker.make(Shop, mobile=self.user.mobile, name="shop1")
        self.order1 = baker.make(Order, user=self.user, shop=self.shop1)
        self.invoice1 = baker.make(Invoice, id=7, user=self.user, order=self.order1)
        self.client = APIClient()
        self.url = reverse("invoices_api:invoice_list_create")

    def test_api_can_create_invoice(self):
        invoice_data = {"user": self.user.pk, "order": self.order1.pk}
        resp = self.client.post(self.url, invoice_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["user"], invoice_data["user"])
        self.assertEqual(resp.data["order"], invoice_data["order"])

    def test_invoice_api_nonexistent_user(self):
        invoice_data = {"user": 2, "order": self.order1.pk}
        resp = self.client.post(self.url, invoice_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_api_nonexistent_order(self):
        invoice_data = {"user": self.user.pk, "order": 1324}
        resp = self.client.post(self.url, invoice_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_api_string_user(self):
        invoice_data = {"user": "invalid", "order": self.order1.pk}
        resp = self.client.post(self.url, invoice_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_api_string_order(self):
        invoice_data = {"user": self.user.pk, "order": "invalid"}
        resp = self.client.post(self.url, invoice_data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_existing_invoice(self):
        resp = self.client.get(self.detail_patch_url(self.invoice1.id))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["id"], self.invoice1.id)

    def test_retrieve_none_existing_invoice(self):
        resp = self.client.get(self.detail_patch_url(102))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(resp.data, None)
