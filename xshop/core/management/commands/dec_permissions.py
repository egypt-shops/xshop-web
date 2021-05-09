from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from xshop.core.utils import UserGroup


GROUP = Group.objects.get(name=UserGroup.DATA_ENTRY_CLERK)
ACTIONS = ["add", "change", "view"]
MODEL = "product"


class Command(BaseCommand):
    def handle(self, *args, **options):
        for action in ACTIONS:
            name = f"Can {action} {MODEL}"
            permission = Permission.objects.get(name=name)
            GROUP.permissions.add(permission)
