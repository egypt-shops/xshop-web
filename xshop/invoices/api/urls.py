from django.urls import path

from . import views

app_name = "invoices_api"

urlpatterns = [
    path("", views.InvoiceListCreateApi.as_view(), name="invoice_list_create"),
]
