from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from .models import Invoice
from xshop.core.utils import UserGroup
from xshop.users.models import User
from xshop.orders.models import Order


def invoice_detail(obj):
    url = reverse("invoices:admin_invoice_detail", args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


def invoice_pdf(obj):
    url = reverse("invoices:admin_invoice_pdf", args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


invoice_pdf.short_discription = "Invoice"


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", invoice_detail, invoice_pdf)
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("-id",)

    def has_view_permission(self, request, obj=None):
        user: User = request.user
        if (
            request.user.is_superuser
            or UserGroup.CASHIER in user.type
            or UserGroup.MANAGER in user.type
        ):
            return True
        return False

    def has_module_permission(self, request):
        user: User = request.user
        if (
            request.user.is_superuser
            or UserGroup.CASHIER in user.type
            or UserGroup.MANAGER in user.type
        ):
            return True
        return False

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     user: User = request.user
    #     if UserGroup.CASHIER in user.type or UserGroup.MANAGER in user.type:
    #         if db_field.name == "order":
    #             kwargs["queryset"] = Order.objects.filter(shop=request.user.shop)
    #         if db_field.name == "user":
    #             kwargs["queryset"] = User.objects.filter(mobile=request.user.mobile)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(InvoiceAdmin, self).get_form(request, obj, **kwargs)
    #     user: User = request.user
    #     if UserGroup.CASHIER in user.type or UserGroup.MANAGER in user.type:
    #         form.base_fields["order"].initial = request.user.id
    #     return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Invoice.objects.all()
        user: User = request.user
        if UserGroup.CASHIER in user.type or UserGroup.MANAGER in user.type:
            orders = Order.objects.filter(shop=request.user.shop)
            return Invoice.objects.filter(order__in=orders)
        raise PermissionDenied(_("You have no access to this data."))
