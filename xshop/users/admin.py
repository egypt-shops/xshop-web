from django import forms
from django.contrib import admin, auth
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

# from rest_framework.authtoken.models import Token, TokenProxy

from xshop.users.forms import UserChangeForm, UserCreationForm
from xshop.users.models import (
    Cashier,
    Customer,
    DataEntryClerk,
    GeneralManager,
    Manager,
    User,
)
from xshop.users.mixins import SuperuserPermissionsMixin
from xshop.core.utils import UserGroup

admin.site.unregister(Group)

# class TokenAdminInline(admin.StackedInline):
#     model = TokenProxy
#     readonly_fields = ("key",)


# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance


@admin.register(Group)
class GroupAdmin(auth.admin.GroupAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ["permissions"]
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

    # permissions
    def has_module_permission(self, request):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def has_view_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def get_queryset(self, request):
        user: User = request.user
        if user.is_superuser:
            return User.objects.all()
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop)
        raise PermissionDenied(_("You have no access to this data."))


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

    def has_view_permission(self, request, obj=None):
        user: User = request.user
        return bool(user.is_superuser)

    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(user.is_superuser)

    def get_queryset(self, request):
        user: User = request.user
        g = Group.objects.get(name=UserGroup.CUSTOMER.title())
        if user.is_superuser:
            return User.objects.filter(groups=g.id)
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop, groups=g.id)
        raise PermissionDenied(_("You have no access to this data."))


@admin.register(Cashier)
class CashierAdmin(UserAdmin):
    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def get_queryset(self, request):
        user: User = request.user
        g = Group.objects.get(name=UserGroup.CASHIER.title())
        if user.is_superuser:
            return User.objects.filter(groups=g.id)
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop, groups=g.id)
        raise PermissionDenied(_("You have no access to this data."))


@admin.register(DataEntryClerk)
class DataEntryClerkAdmin(UserAdmin):
    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def get_queryset(self, request):
        user: User = request.user
        g = Group.objects.get(name=UserGroup.DATA_ENTRY_CLERK.title())
        if user.is_superuser:
            return User.objects.filter(groups=g.id)
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop, groups=g.id)
        raise PermissionDenied(_("You have no access to this data."))


@admin.register(Manager)
class ManagerAdmin(UserAdmin):
    def has_add_permission(self, request, obj=None):
        user: User = request.user
        return bool(
            user.is_superuser or user.type[0] == UserGroup.GENERAL_MANAGER.title()
        )

    def get_queryset(self, request):
        user: User = request.user
        g = Group.objects.get(name=UserGroup.MANAGER.title())
        if user.is_superuser:
            return User.objects.filter(groups=g.id)
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop, groups=g.id)
        raise PermissionDenied(_("You have no access to this data."))


@admin.register(GeneralManager)
class GeneralManagerAdmin(UserAdmin):
    def get_queryset(self, request):
        user: User = request.user
        g = Group.objects.get(name=UserGroup.GENERAL_MANAGER.title())
        if user.is_superuser:
            return User.objects.filter(groups=g.id)
        if user.type and user.type[0] == UserGroup.GENERAL_MANAGER.title():
            return User.objects.filter(shop=user.shop, groups=g.id)
        raise PermissionDenied(_("You have no access to this data."))
