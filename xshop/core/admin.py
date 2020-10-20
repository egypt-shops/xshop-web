from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import Shop, Invoice, Order, OrderItem, PricingPlan, Product


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "added_by", "name", "price", "stock", "shop")
    list_display_links = ("name",)
    list_filter = ("price",)
    search_fields = ("name",)
    ordering = ("-id",)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    actions = ["export_as_csv"]
    export_as_csv.short_description = "Export selected products"


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 1
    max_num = 1

    list_display = ("id", "shop", "price", "name")
    list_display_links = ("name",)
    list_filter = "price"
    search_fields = "name"
    ordering = ("-id",)


class ShopAdmin(admin.ModelAdmin):
    model = Shop
    inlines = [
        PricingPlanInline,
    ]
    list_display = ("id", "mobile", "name", "dashboard_modules")
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("-id",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

    list_display = ("id", "order", "product", "quantity")
    list_display_links = ("order",)
    list_filter = "quantity"
    search_fields = "order"
    ordering = ("-id",)


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice

    list_display = (
        "id",
        "user",
    )
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("-id",)


class Orderadmin(admin.ModelAdmin):
    model = Order

    list_display = ("id", "user", "shop")
    list_display_links = ("user",)
    list_filter = ("user", "shop")
    search_fields = ("user", "shop")
    ordering = ("-id",)

    inlines = [
        OrderItemInline,
    ]


admin.site.register(Shop, ShopAdmin)
admin.site.register(Order, Orderadmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product, ProductAdmin)
