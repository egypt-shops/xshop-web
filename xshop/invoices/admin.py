from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Invoice


def invoice_detail(obj):
    url = reverse("invoices:admin_invoice_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", invoice_detail)
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("-id",)
