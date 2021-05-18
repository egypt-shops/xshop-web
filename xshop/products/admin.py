import csv
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from xshop.shops.models import Shop
from .models import Product
from xshop.core.utils import UserGroup
from xshop.users.models import User


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "added_by", "name", "price", "stock", "shop")
    list_display_links = ("id", "name")
    list_filter = ("price",)
    search_fields = ("name",)
    ordering = ("-id",)

    def has_view_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            request.user.is_superuser
            or user.type[0]
            in [
                UserGroup.GENERAL_MANAGER.title(),
                UserGroup.DATA_ENTRY_CLERK.title(),
            ]
        )

    def has_module_permission(self, request):
        user: User = request.user
        return bool(
            request.user.is_superuser
            or user.type[0]
            in [
                UserGroup.GENERAL_MANAGER.title(),
                UserGroup.DATA_ENTRY_CLERK.title(),
            ]
        )

    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser
            or user.type[0]
            in [UserGroup.DATA_ENTRY_CLERK.title(), UserGroup.GENERAL_MANAGER.title()]
        )

    def has_change_permission(self, request, obj=None):
        user: User = request.user
        # breakpoint()
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user: User = request.user
        if user.type:
            if (
                user.type[0] == UserGroup.DATA_ENTRY_CLERK.title()
                and db_field.name == "added_by"
            ):
                kwargs["queryset"] = User.objects.filter(id=user.id)
            if (
                user.type[0] == UserGroup.GENERAL_MANAGER.title()
                and db_field.name == "added_by"
            ):
                kwargs["queryset"] = User.objects.filter(shop=user.shop.id)
            if (
                user.type[0]
                in [
                    UserGroup.GENERAL_MANAGER.title(),
                    UserGroup.DATA_ENTRY_CLERK.title(),
                ]
                and db_field.name == "shop"
            ):
                kwargs["queryset"] = Shop.objects.filter(id=user.shop.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        user: User = request.user
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if user.type and user.type[0] in [
            UserGroup.GENERAL_MANAGER.title(),
            UserGroup.DATA_ENTRY_CLERK.title(),
        ]:
            form.base_fields["added_by"].initial = user
            form.base_fields["shop"].initial = user.shop
        return form

    def get_queryset(self, request):
        user: User = request.user
        if user.is_superuser:
            return Product.objects.all()
        if user.type and user.type[0] in [
            UserGroup.GENERAL_MANAGER.title(),
            UserGroup.DATA_ENTRY_CLERK.title(),
        ]:
            return Product.objects.filter(shop=user.shop)
        raise PermissionDenied(_("You have no access to this data."))

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    actions = ["export_as_csv"]
    export_as_csv.short_description = "Export selected products"


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3
    list_display = ("id", "added_by", "name", "price", "stock", "shop")
    list_display_links = ("id", "name")
    list_filter = ("price",)
    search_fields = ("name",)
    ordering = ("-id",)
