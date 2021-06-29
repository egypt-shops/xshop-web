import csv
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.urls import path
from django.shortcuts import render, redirect, reverse
from django import forms
from django.contrib import messages

import codecs

from xshop.shops.models import Shop
from .models import Product
from xshop.core.utils import UserGroup
from xshop.users.models import User


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


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

    change_list_template = "admin/product_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("admin/import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            imported_file = request.FILES["csv_file"]
            csv_file = csv.DictReader(codecs.iterdecode(imported_file, "utf-8"))
            column_names = [
                "name",
                "price",
                "stock",
                "barcode",
                "country_id",
                "manufacturer_id",
                "number_id",
            ]
            for name in column_names:
                if name not in csv_file.fieldnames:
                    messages.error(
                        request,
                        "Your csv file does not contain '{}' column".format(name),
                    )
                    return redirect(reverse("admin:products_product_changelist"))
            for line in csv_file:
                if not line["price"].isnumeric():
                    messages.error(
                        request,
                        "the product '{}' has no numeric price".format(line["name"]),
                    )
                    return redirect(reverse("admin:products_product_changelist"))
                Product.objects.create(
                    name=line["name"],
                    price=line["price"],
                    stock=line["stock"],
                    barcode=line["barcode"],
                    country_id=line["country_id"],
                    manufacturer_id=line["manufacturer_id"],
                    number_id=line["number_id"],
                    added_by=request.user,
                    shop=request.user.shop,
                )
            # file_cleaned = [x.split(',') for x in csv_file.decode('ascii').split('\r\n')]
            self.message_user(request, "Your csv file has been imported")
            return redirect(reverse("admin:products_product_changelist"))
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 3
    list_display = ("id", "added_by", "name", "price", "stock", "shop")
    list_display_links = ("id", "name")
    list_filter = ("price",)
    search_fields = ("name",)
    ordering = ("-id",)
