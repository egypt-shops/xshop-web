from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.dispatch import receiver

from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField


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
    class Types(models.TextChoices):
        """User types in our system"""

        CUSTOMER = "CUSTOMER", "Customer"
        CASHIER = "CASHIER", "Cashier"
        DATA_ENTRY_CLERK = "DATA_ENTRY_CLERK", "Data Entry Clerk"
        MANAGER = "MANAGER", "Manager"
        SUB_MANAGER = "SUB_MANAGER", "Sub Manager"

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

    # optional
    type = MultiSelectField(choices=Types.choices, null=True, blank=True)

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    objects = UserManager()

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

    # def has_module_permission(self) -> bool:
    #     """Customize permission based on user's type"""

    # if self.type:
    #     if self.type in ("MANAGER", "SUB_MANAGER"):
    #         return
    #     if self.type in ("CUSTOMER",):
    #         return False


# Create auth_token upon user creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# =========================================== Other Users ModelManagers
class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=[User.Types.CUSTOMER])

    def create(self, **kwargs):
        kwargs.update({"type": [User.Types.CUSTOMER]})
        return super().create(**kwargs)


class CashierManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=[User.Types.CASHIER])

    def create(self, **kwargs):
        kwargs.update({"type": [User.Types.CASHIER]})
        return super().create(**kwargs)


class DataEntryClerkManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=[User.Types.DATA_ENTRY_CLERK])

    def create(self, **kwargs):
        kwargs.update({"type": [User.Types.DATA_ENTRY_CLERK]})
        return super().create(**kwargs)


class SubManagerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=[User.Types.SUB_MANAGER])

    def create(self, **kwargs):
        kwargs.update({"type": [User.Types.SUB_MANAGER]})
        return super().create(**kwargs)


class ManagerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=[User.Types.MANAGER])

    def create(self, **kwargs):
        kwargs.update({"type": [User.Types.MANAGER]})
        return super().create(**kwargs)


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


class DataEntryClerk(User):
    class Meta:
        proxy = True

    objects = DataEntryClerkManager()

    verbose_name = "Data Entry Clerk"
    verbose_name_plural = "Data Entry Clerks"


class SubManager(User):
    class Meta:
        proxy = True

    objects = SubManagerManager()

    verbose_name = "Sub Manger"
    verbose_name_plural = "Sub Managers"


class Manager(User):
    class Meta:
        proxy = True

    objects = ManagerManager()

    verbose_name = "Manger"
    verbose_name_plural = "Managers"
