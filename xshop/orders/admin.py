from django.contrib import admin

from xshop.core.utils import UserGroup
from xshop.users.models import User
from xshop.shops.models import Shop
from xshop.products.models import Product
from xshop.invoices.models import Invoice
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2

    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(request.user.is_superuser or UserGroup.CASHIER in user.type)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user: User = request.user
        if UserGroup.CASHIER in user.type:
            if db_field.name == "product":
                kwargs["queryset"] = Product.objects.filter(shop=request.user.shop)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ("id", "user", "shop")
    list_display_links = ("id", "user")
    search_fields = ("user__name", "user__mobile", "shop__name", "shop__mobile")
    ordering = ("-id",)
    # readonly_fields = ('shop', )

    # save methods
    def save_model(self, request, obj, form, change):
        user: User = request.user
        if UserGroup.CASHIER in user.type:
            obj.shop = user.shop
            obj.shop = user
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        user: User = request.user
        if UserGroup.CASHIER in user.type:
            Invoice.objects.create(user=user, order=obj)
        return super().response_add(request, obj, post_url_continue=post_url_continue)

    # UI methods
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     user: User = request.user
    #     if UserGroup.CASHIER in user.type:
    #         if db_field.name == "shop":
    #             kwargs["queryset"] = Shop.objects.filter(id=request.user.shop.id)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        user: User = request.user
        if UserGroup.CASHIER in user.type:
            self.exclude = ('shop', 'user',)
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        return form

    # permissions
    def has_module_permission(self, request):
        user: User = request.user
        if request.user.is_superuser or UserGroup.CASHIER in user.type:
            return True
        return False

    def has_add_permission(self, request, obj=None):
        user: User = request.user
        if request.user.is_superuser or UserGroup.CASHIER in user.type:
            return True
        return False
