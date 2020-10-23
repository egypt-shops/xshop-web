from django.urls import path

from . import views

app_name = "invoices_api"

urlpatterns = [
    path(
        "<int:invoice_id>/",
        views.InvoiceDetailPatchApi.as_view(),
        name="invoice_detail_patch",
    ),
    path("", views.InvoiceListCreateApi.as_view(), name="invoice_list_create"),
]
