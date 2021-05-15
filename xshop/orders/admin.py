from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ("id", "user", "shop")
    list_display_links = ("id", "user")
    search_fields = ("user__name", "user__mobile", "shop__name", "shop__mobile")
    ordering = ("-id",)
