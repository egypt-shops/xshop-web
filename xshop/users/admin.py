from django import forms
from django.contrib import admin, auth
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

# from rest_framework.authtoken.models import Token, TokenProxy

from .forms import UserChangeForm, UserCreationForm
from .models import Cashier, Customer, DataEntryClerk, GeneralManager, Manager, User
from .mixins import SuperuserPermissionsMixin


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
