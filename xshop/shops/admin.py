from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from xshop.products.admin import ProductInline
from .models import PricingPlan, Shop
from xshop.core.utils import UserGroup
from xshop.users.models import User


class PricingPlanInline(admin.TabularInline):
    model = PricingPlan
    extra = 1
    max_num = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = (ProductInline, PricingPlanInline)
    list_display = ("id", "mobile", "name", "dashboard_modules")
    list_editable = ("name",)
    list_display_links = ("id", "mobile")
    search_fields = ("name", "mobile")
    ordering = ("-id",)

    def has_module_permission(self, request):
        user: User = request.user
        try:
            return bool(
                user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
            )
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def has_change_permission(self, request, obj=None):
        user: User = request.user
        # breakpoint()
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def get_queryset(self, request):
        user: User = request.user
        if user.is_superuser:
            return Shop.objects.all()
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return Shop.objects.filter(id=user.shop.id)
        raise PermissionDenied(_("You have no access to this data."))
