from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from xshop.core.utils import UserGroup


GROUP = Group.objects.get(name=UserGroup.CASHIER)
ACTIONS = ["add", "view"]
MODELS = ["order", "order item"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for action in ACTIONS:
            for model in MODELS:
                name = f"Can {action} {model}"
                permission = Permission.objects.get(name=name)
                GROUP.permissions.add(permission)

        permission = Permission.objects.get(name="Can view invoice")
        GROUP.permissions.add(permission)
