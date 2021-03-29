from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from xshop.core.utils import UserGroup


# =========================================== User ModelManager
class UserManager(BaseUserManager):
    """
    User model manager where mobile is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, mobile, password, **extra_fields):
        """
        Create and save a User with the given mobile and password.
        """
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """
        Create and save a SuperUser with the given mobile and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(mobile, password, **extra_fields)


# =========================================== User Model
class User(AbstractUser, TimeStampedModel):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # Removed from base class
    first_name = None
    last_name = None
    username = None

    # required
    name = models.CharField(max_length=255, blank=True)
    mobile = PhoneNumberField(unique=True)

    # Settings
    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    # Model Managers
    objects = UserManager()

    # Relations
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.SET_NULL, null=True, blank=True
    )

    # Calculated Properties
    @property
    def roles(self):
        """To be used in admin and serializers without overriding the `groups` M2M field"""
        return [name for name in self.groups.values_list("name", flat=True)]

    @property
    def type(self):
        """Backward compatible alternative to `type` field"""
        return self.roles

    def __str__(self) -> str:
        return self.mobile.as_national.replace(" ", "")

    def __repr__(self) -> str:
        if self.name:
            return f"<User {self.id}: {str(self)} - {self.name}>"
        return f"<User {self.id}: {str(self)}>"

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        name_list = self.name.split(" ")
        if len(name_list) > 0:
            return name_list[0]
        return ""

    # validating that manager have a shop
    def clean(self, *args, **kwargs):
        # custom validations here
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# =========================================== Other Users ModelManagers
class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=UserGroup.CUSTOMER)


class CashierManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=UserGroup.CASHIER)


class DataEntryClerkManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=UserGroup.DATA_ENTRY_CLERK)


class ManagerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=UserGroup.MANAGER)


class GeneralManagerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(groups__name=UserGroup.GENERAL_MANAGER)


# =========================================== Other Users Models
class Customer(User):
    class Meta:
        proxy = True

    objects = CustomerManager()

    verbose_name = "Customer"
    verbose_name_plural = "Customers"


class Cashier(User):
    class Meta:
        proxy = True

    objects = CashierManager()

    verbose_name = "Cashier"
    verbose_name_plural = "Cashiers"

    def clean(self, *args, **kwargs):
        if not self.shop:
            raise ValidationError(_("Cashier must have a shop."))
        super().clean(*args, **kwargs)


class DataEntryClerk(User):
    class Meta:
        proxy = True

    objects = DataEntryClerkManager()

    verbose_name = "Data Entry Clerk"
    verbose_name_plural = "Data Entry Clerks"

    def clean(self, *args, **kwargs):
        if not self.shop:
            raise ValidationError(_("Data Entry Clerk must have a shop."))
        super().clean(*args, **kwargs)


class Manager(User):
    class Meta:
        proxy = True

    objects = ManagerManager()

    verbose_name = "Sub Manger"
    verbose_name_plural = "Sub Managers"

    def clean(self, *args, **kwargs):
        if not self.shop:
            raise ValidationError(_("Manager must have a shop."))
        super().clean(*args, **kwargs)


class GeneralManager(User):
    class Meta:
        proxy = True

    objects = GeneralManagerManager()

    verbose_name = "Manger"
    verbose_name_plural = "Managers"

    def clean(self, *args, **kwargs):
        if not self.shop:
            raise ValidationError(_("General Manager must have a shop."))
        super().clean(*args, **kwargs)
