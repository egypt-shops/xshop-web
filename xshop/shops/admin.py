from django.contrib import admin

from xshop.products.admin import ProductInline

from .models import PricingPlan, Shop
from ..users.mixins import ManagerFullPermissionMixin


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 1
    max_num = 1


@admin.register(Shop)
class ShopAdmin(ManagerFullPermissionMixin, admin.ModelAdmin):
    inlines = (ProductInline, PricingPlanInline)
    list_display = ("id", "mobile", "name", "dashboard_modules")
    list_editable = ("name",)
    list_display_links = ("id", "mobile")
    search_fields = ("name", "mobile")
    ordering = ("-id",)
