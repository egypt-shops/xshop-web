from django.urls import path

from .views import admin_invoice_detail, admin_invoice_pdf

app_name = "invoices"


urlpatterns = [
    path(
        "admin/invoices/<int:invoice_id>/",
        admin_invoice_detail,
        name="admin_invoice_detail",
    ),
    path(
        "admin/invoices/<int:invoice_id>/pdf/",
        admin_invoice_pdf,
        name="admin_invoice_pdf",
    ),
]
