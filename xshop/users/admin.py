from django.contrib import admin, auth

from .forms import UserChangeForm, UserCreationForm
from .models import Cashier, Customer, DataEntryClerk, GeneralManager, Manager, User
from .mixins import SuperuserPermissionsMixin

# from rest_framework.authtoken.models import Token, TokenProxy


# class TokenAdminInline(admin.StackedInline):
#     model = TokenProxy
#     readonly_fields = ("key",)


@admin.register(User)
class UserAdmin(SuperuserPermissionsMixin, auth.admin.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("id", "mobile", "email", "name", "roles", "is_staff", "is_active")
    list_display_links = ("id", "mobile")
    list_filter = ("is_staff", "is_active")
    search_fields = ("mobile", "email", "name")
    ordering = ("-id",)

    fieldsets = (
        (
            None,
            {"fields": ("mobile", "email", "name", "password", "shop")},
        ),  # "roles",
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
                    # "roles",
                    "shop",
                ),
            },
        ),
    )

    # inlines = (TokenAdminInline,)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    fieldsets = None
    fields = ("mobile", "email", "name", "password")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "mobile",
                    "password1",
                    "password2",
                    "is_active",
                ),
            },
        ),
    )

    def has_add_permission(self, request, obj=None):
        if request.user.is_authenticated and request.user.is_superuser:
            return True


@admin.register(Cashier)
class CashierAdmin(UserAdmin):
    ...


@admin.register(DataEntryClerk)
class DataEntryClerkAdmin(UserAdmin):
    ...


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    ...


@admin.register(GeneralManager)
class GeneralManagerAdmin(UserAdmin):
    ...
