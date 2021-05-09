from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from xshop.core.utils import UserGroup


GROUP = Group.objects.get(name=UserGroup.GENERAL_MANAGER)
APPS = {
    "invoices": ["invoice"],
    "orders": ["order", "order item"],
    "products": ["product"],
    "users": ["general manager", "manager", "data entry clerk", "cashier"],
    "shops": ["shop"],
}
ACTIONS = ["add", "change", "delete", "view"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for app in APPS:
            if app != "shops":
                for model in APPS.get(app):
                    if app == "users" and model == "general manager":
                        permission = Permission.objects.get(
                            name="Can view general manager"
                        )
                        GROUP.permissions.add(permission)
                        permission = Permission.objects.get(
                            name="Can change general manager"
                        )
                        GROUP.permissions.add(permission)
                    else:
                        for action in ACTIONS:
                            name = f"Can {action} {model}"
                            permission = Permission.objects.get(name=name)
                            GROUP.permissions.add(permission)
            else:
                permission = Permission.objects.get(name="Can view shop")
                GROUP.permissions.add(permission)
                permission = Permission.objects.get(name="Can change shop")
                GROUP.permissions.add(permission)
