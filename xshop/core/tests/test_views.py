from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import Group


class CreateGroupsTests(TestCase):
    def test_retrieve_existing_groups(self):
        self.assertEqual(Group.objects.all().count(), 0)
        call_command("create_groups")
        self.assertEqual(Group.objects.all().count(), 5)
