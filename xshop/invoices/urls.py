from django.urls import path
from .views import admin_invoice_detail

app_name = "core"


urlpatterns = [
    path(
        "admin/invoices/<int:invoice_id>/",
        admin_invoice_detail,
        name="admin_invoice_detail",
    )
]
