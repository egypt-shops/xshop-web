from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

from .forms import UserCreationForm, UserChangeForm
from .models import (
    User,
    Customer,
    Cashier,
    DataEntryClerk,
    Manager,
    SubManager,
)


class TokenInline(admin.StackedInline):
    model = Token


@admin.register(User)
class UserAdmin(OriginalUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("id", "mobile", "email", "name", "is_staff", "is_active")
    list_display_links = ("mobile",)
    list_filter = ("is_staff", "is_active")
    search_fields = ("mobile", "email", "name")
    ordering = ("-id",)

    readonly_fields = ("type",)

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

    inlines = (TokenInline,)


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    ...


@admin.register(Cashier)
class CashierAdmin(UserAdmin):
    readonly_fields = ()


@admin.register(DataEntryClerk)
class DataEntryClerkAdmin(UserAdmin):
    ...


@admin.register(SubManager)
class SubManagerAdmin(UserAdmin):
    ...


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    ...


admin.site.unregister(Group)
