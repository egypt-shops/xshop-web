import logging

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from xshop.core.utils import UserGroup
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = [
    UserGroup.CUSTOMER,
    UserGroup.CASHIER,
    UserGroup.DATA_ENTRY_CLERK,
    UserGroup.GENERAL_MANAGER,
    UserGroup.MANAGER,
]
APPS = {
    "invoices": ["invoice"],
    "orders": ["order", "orderitem"],
    "products": ["product"],
    "users": ["generalmanager", "manager", "dataentryclerk", "cashier"],
    "shops": ["shop"],
}
ACTIONS = ["add", "change", "delete", "view"]


class Command(BaseCommand):
    def handle(self, *args, **options):

        for app in APPS:
            for model in APPS.get(app):
                ct = ContentType.objects.get(app_label=app, model=model)

                for action in ACTIONS:
                    name = "Can {} {}".format(action, model)
                    self.stdout.write("Creating {}".format(name))
                    code_name = f"{app}.{action}_{model}"

                    if Permission.objects.filter(codename=code_name):
                        continue
                    else:
                        try:
                            permission = Permission.objects.create(
                                codename=code_name, content_type=ct
                            )
                        except Permission.DoesNotExist:
                            logging.warning(
                                "Permission not found with name '{}'.".format(name)
                            )
                            continue

                        for group in GROUPS:
                            new_group, created = Group.objects.get_or_create(name=group)
                            new_group.permissions.add(permission)
