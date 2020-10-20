import logging

# from collections import OrderedDict

# from django.urls import path
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy as _

# from django_admin_listfilter_dropdown.filters import DropdownFilter

import csv
from django.http import HttpResponse

from .models import Shop, Invoice, Order, OrderItem, PricingPlan, Product

logger = logging.getLogger(__name__)


class CoreAdmin(AdminSite):
    """Django Admin customizations"""

    # Text to put at the end of each page's <title>.
    site_title = _("Egypt Shops Dashboard")

    # Text to put in each page's <h1> (and above login form).
    site_header = _("Egypt Shops Dashboard")

    # Text to put at the top of the admin index page.
    index_title = _("Egypt Shops Dashboard")

    def get_urls(self):
        """Customize returned URLs"""
        urls = super(CoreAdmin, self).get_urls()

        # Add custom Admin urls here
        # custom_urls = []

        return urls  # + custom_urls

    # def prepare_components_data(self, user):
    #     """Prepare dashboard components based on logged-in user

    #     if super user we show him all available data.
    #     if shop manager, we show him data related to his/her shop only."""

    #     return {"stat_list": [], "chart_list": []}

    def index(self, request):
        """Customize Admin Index page before presenting"""
        # extra_context = self.prepare_components_data(request.user)
        # Update extra_context with new variables
        return super().index(request)  # , extra_context)


class CustomPermissionsMixin:
    """Custom Permissions to customize who sees what"""

    def has_view_permission(self, request, obj=None):
        # User must be authenticated to view any object
        if request.user.is_authenticated:
            # Super user can always view objects
            if request.user.is_superuser:
                return True
            # Other users can allowed objects only
            return request.user.has_module_permission(self.model.__name__)

    def has_module_permission(self, request):
        # User must be authenticated to view/access any admin module in index page
        if request.user.is_authenticated:
            # Super user can always see all modules
            if request.user.is_superuser:
                return True
            # User must be Manager to view/edit SubManager
            if (
                request.user.type in ("MANAGER",)
                and self.model.__name__ == "SubManagerAdmin"
            ):
                return True

            # User must be Manager/SubManager to have any module permisssion
            # Module permissions are specified per user
            if request.user.type in ("MANAGER", "SUB_MANAGER"):
                return request.user.has_module_permission(self.model.__name__)

    def has_add_permission(self, request, obj=None):
        # User must be authenticated to add any new objects
        if request.user.is_authenticated:
            # A superuser can add any object
            if request.user.is_superuser:
                return True
            # Any other user must have the permission to add an object
            return request.user.has_module_permission(self.model.__name__)

    def has_change_permission(self, request, obj=None):
        # User must be authenticated to change objects
        if request.user.is_authenticated:
            # A superuser can change any object
            if request.user.is_superuser:
                return True
            # Any other user must have the permission to change an object
            return request.user.has_module_permission(self.model.__name__)

    def has_delete_permission(self, request, obj=None):
        # User must be authenticated to delete objects
        if request.user.is_authenticated:
            # A superuser can delete any object
            if request.user.is_superuser:
                return True
            # Any other user must have the permission to delete an object
            return request.user.has_module_permission(self.model.__name__)

    def lookup_allowed(self, key, value):
        # allow all lookups for now
        return True


class CustomStackedInline(CustomPermissionsMixin, admin.StackedInline):
    """Base TabularInline for the project's TabularInlines"""


class CustomTabularInline(CustomPermissionsMixin, admin.TabularInline):
    """Base TabularInline for the project's TabularInlines"""


class CustomModelAdmin(CustomPermissionsMixin, admin.ModelAdmin):
    """Base ModelAdmin for the project's ModelAdmins"""

    # for persisting filter and search values in admin change list view pagination
    def changelist_view(self, request, extra_context={}):
        params = dict(request.GET.items())
        extra_context.update({"params": params})
        return super().changelist_view(request, extra_context)


# TODO decide if we need it or what
# class ShopBasedDropdownFilter(DropdownFilter):
#     def __init__(self, field, request, params, model, model_admin, field_path):
#         super().__init__(field, request, params, model, model_admin, field_path)

#         parent_model, reverse_path = reverse_field_path(model, field_path)
#         # Obey parent ModelAdmin queryset when deciding which options to show
#         if model == parent_model:
#             queryset = model_admin.get_queryset(request)
#         else:
#             queryset = parent_model._default_manager.all()
#         if hasattr(model, "shop"):
#             # we only need it in case of community admin this why we use "not"
#             if not request.user.is_superuser:
#                 self.lookup_choices = (
#                     queryset.filter(shop=request.user.shop)
#                     .distinct()
#                     .order_by(field.name)
#                     .values_list(field.name, flat=True)
#                 )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ("id", "added_by", "name", "price", "stock", "shop")
    list_display_links = ("id", "name")
    list_filter = ("price",)
    search_fields = ("name",)
    ordering = ("-id",)

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


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("-id",)


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
