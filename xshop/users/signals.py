from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from xshop.core.utils import UserGroup
from xshop.users.models import (
    Cashier,
    Customer,
    DataEntryClerk,
    GeneralManager,
    Manager,
)

# ====================== add is_staff in pre_save


@receiver(pre_save, sender=Cashier)
def staff_cashiers(sender, instance, **kwargs):
    instance.is_staff = True


@receiver(pre_save, sender=DataEntryClerk)
def staff_data_entry(sender, instance, **kwargs):
    instance.is_staff = True


@receiver(pre_save, sender=Manager)
def staff_managers(sender, instance, **kwargs):
    instance.is_staff = True


@receiver(pre_save, sender=GeneralManager)
def staff_general_managers(sender, instance, **kwargs):
    instance.is_staff = True


# ======================  A Token for each user upon creation
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# ====================== Add User to corresponding group upon creation
@receiver(post_save, sender=Customer)
def group_customers(sender, instance=None, created=False, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=UserGroup.CUSTOMER)
        instance.groups.add(group)


@receiver(post_save, sender=Cashier)
def group_cashiers(sender, instance=None, created=False, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=UserGroup.CASHIER)
        instance.groups.add(group)


@receiver(post_save, sender=DataEntryClerk)
def group_data_entry(sender, instance=None, created=False, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=UserGroup.DATA_ENTRY_CLERK)
        instance.groups.add(group)


@receiver(post_save, sender=Manager)
def group_managers(sender, instance=None, created=False, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=UserGroup.MANAGER)
        instance.groups.add(group)


@receiver(post_save, sender=GeneralManager)
def group_general_managers(sender, instance=None, created=False, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name=UserGroup.GENERAL_MANAGER)
        instance.groups.add(group)
