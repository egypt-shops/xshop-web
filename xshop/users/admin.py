from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group

# from rest_framework.authtoken.models import Token, TokenProxy

from .forms import UserCreationForm, UserChangeForm
from .models import (
    User,
    Customer,
    Cashier,
    DataEntryClerk,
    Manager,
    SubManager,
)


# class TokenAdminInline(admin.StackedInline):
#     model = TokenProxy
#     readonly_fields = ("key",)


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("id", "mobile", "email", "name", "type", "is_staff", "is_active")
    list_display_links = ("id", "mobile")
    list_filter = ("is_staff", "is_active")
    search_fields = ("mobile", "email", "name")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("mobile", "email", "name", "password", "type")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "mobile",
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "type",
                ),
            },
        ),
    )

    # inlines = (TokenAdminInline,)

    # custom permissions
    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    readonly_fields = ("type",)
    fieldsets = None
    fields = ("mobile", "email", "name", "password")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile", "password1", "password2", "is_active",),
            },
        ),
    )

    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    # def has_add_permission(self, request, obj=None):
    #     if request.user.is_authenticated and request.user.is_superuser:
    #         return True


@admin.register(Cashier)
class CashierAdmin(UserAdmin):
    readonly_fields = ("type",)

    # Superuser only has the permissions for the Users Module
    def has_module_permission(self, request):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_view_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True

    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.type == [User.Types.MANAGER]
        ):
            return True


@admin.register(DataEntryClerk)
class DataEntryClerkAdmin(UserAdmin):
    readonly_fields = ("type",)


@admin.register(SubManager)
class SubManagerAdmin(UserAdmin):
    readonly_fields = ("type",)


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    readonly_fields = ("type",)


admin.site.unregister(Group)
