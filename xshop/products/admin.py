import csv
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

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

    def get_queryset(self, request):
        user: User = request.user
        if user.is_superuser:
            return Product.objects.all()
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
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
