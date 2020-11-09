from ..shops.models import Shop
from .models import User


class ManagerFullPermissionMixin(object):
    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True


class ManagerViewPermissionMixin(object):
    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True


class ManagerViewUpdatePermissionMixin(object):
    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.type == [User.Types.MANAGER]
            and Shop.objects.filter(mobile=request.user.mobile).exists()
        ):
            return True
