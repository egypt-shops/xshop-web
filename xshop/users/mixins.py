from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SuperuserPermissionsMixin:
    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        return bool(request.user.is_authenticated and request.user.is_superuser)

    def has_view_permission(self, request, obj=None):
        return bool(request.user.is_authenticated and request.user.is_superuser)

    def has_change_permission(self, request, obj=None):
        return bool(request.user.is_authenticated and request.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_authenticated and request.user.is_superuser)

    def has_add_permission(self, request, obj=None):
        return bool(request.user.is_authenticated and request.user.is_superuser)


class ShopRequiredMixin(object):
    """
    Making sure that Manager, GM, DEC, Cashier are connected to shop when created
    """

    def clean(self, *args, **kwargs):
        if not self.shop:
            raise ValidationError(_(f"{self.verbose_name} must have a shop."))
        super().clean(*args, **kwargs)
