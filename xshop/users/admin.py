from django.contrib import admin, auth
from django.contrib.auth.models import Group

# from rest_framework.authtoken.models import Token, TokenProxy

from .forms import UserChangeForm, UserCreationForm
from .models import Cashier, Customer, DataEntryClerk, GeneralManager, Manager, User
from .mixins import SuperuserPermissionsMixin


admin.site.unregister(Group)

# class TokenAdminInline(admin.StackedInline):
#     model = TokenProxy
#     readonly_fields = ("key",)


@admin.register(Group)
class GroupAdmin(auth.admin.GroupAdmin):
    readonly_fields = ("name",)


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

    # inlines = (GroupAdminInline,)  # TokenAdminInline,)


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
