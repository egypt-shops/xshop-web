from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel

from .managers import UserManager


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

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self) -> str:
        return self.name

    def get_short_name(self) -> str:
        name_list = self.name.split(" ")
        if len(name_list) > 0:
            return name_list[0]
        return ""

    def __str__(self) -> str:
        return self.mobile.as_national.replace(" ", "")

    def __repr__(self) -> str:
        if self.name:
            return f"<User {self.id}: {str(self)} - {self.name}>"
        return f"<User {self.id}: {str(self)}>"
