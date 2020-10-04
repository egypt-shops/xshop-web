from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField


class Shop(TimeStampedModel):
    mobile = PhoneNumberField()
    name = models.CharField(max_length=255)
    dashboard_modules = MultiSelectField(choices=settings.DASHBOARD_MODULES, blank=True)
