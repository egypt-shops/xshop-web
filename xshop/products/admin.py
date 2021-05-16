import csv

from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from xshop.core.utils import UserGroup
from xshop.users.models import User
from xshop.shops.models import Shop

from .models import Product


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
        if request.user.is_superuser or UserGroup.DATA_ENTRY_CLERK in user.type:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        user: User = request.user
        if request.user.is_superuser or UserGroup.DATA_ENTRY_CLERK in user.type:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        user: User = request.user
        if request.user.is_superuser or UserGroup.DATA_ENTRY_CLERK in user.type:
            return True
        return False

    def has_module_permission(self, request):
        user: User = request.user
        if request.user.is_superuser or UserGroup.DATA_ENTRY_CLERK in user.type:
            return True
        return False

    def save_model(self, request, obj, form, change):
        obj.shop = request.user.shop
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            kwargs["queryset"] = Shop.objects.filter(id=request.user.shop.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["shop"].initial = request.user.shop
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Product.objects.all()
        if "General Manager" in request.user.type:
            return Product.objects.filter(shop=request.user.shop)
        if UserGroup.DATA_ENTRY_CLERK in request.user.type:
            return Product.objects.filter(shop=request.user.shop)

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
