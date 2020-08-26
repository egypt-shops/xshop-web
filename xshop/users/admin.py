from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(OriginalUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    list_display = ("id", "mobile", "email", "name", "is_staff", "is_active")
    list_display_links = ("mobile",)
    list_filter = ("is_staff", "is_active")
    search_fields = ("mobile", "email", "name")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("mobile", "email", "name", "password")}),
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
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
