from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("-id",)
