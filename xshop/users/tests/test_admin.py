from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from model_bakery import baker

from ..admin import UserAdmin
from ..models import User
from ..forms import UserChangeForm


class MockRequest:
    GET = ""

    def get(self):
        request_factory = RequestFactory()
        return request_factory.get("/admin")


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class UserAdminTests(TestCase):
    def setUp(self) -> None:
        self.site = AdminSite()
        self.model_admin = UserAdmin(User, self.site)

        # users
        self.superuser = baker.make(User, mobile="01010092181", is_superuser=True)
        self.test_user = baker.make(User, mobile="01010092182")

        # request
        self.request = MockRequest()
        self.request.user = self.superuser

        # attr values
        self.superuser_user_list_display = (
            "id",
            "mobile",
            "email",
            "name",
            "is_staff",
            "is_active",
        )
        self.superuser_list_filter = ("is_staff", "is_active")

    def test_superuser_user_admin_str(self):
        self.assertEqual(str(self.model_admin), "users.UserAdmin")

    def test_superuser_queryset(self):
        self.assertEqual(
            list(self.model_admin.get_queryset(self.request).order_by("-id")),
            list(User.objects.all().order_by("-id")),
        )

    def test_superuser_change_form(self):
        # we are trying to access a form that never exists
        self.request.user = self.superuser
        form = self.model_admin.form(self.request)
        self.assertIsNotNone(form)
        self.assertTrue(isinstance(form, UserChangeForm))

    def test_superuser_list_display(self):
        self.assertEqual(
            self.model_admin.get_list_display(self.request),
            self.superuser_user_list_display,
        )

    def test_superuser_list_display_links(self):
        superuser_user_list_display_links = ("mobile",)
        self.assertEqual(
            self.model_admin.get_list_display_links(
                self.request, self.superuser_user_list_display
            ),
            superuser_user_list_display_links,
        )

    def test_superuser_list_filter(self):
        self.assertEqual(
            self.model_admin.get_list_filter(self.request), self.superuser_list_filter,
        )

    def test_superuser_search_fields(self):
        self.assertEqual(
            self.model_admin.get_search_fields(self.request),
            ("mobile", "email", "name"),
        )

    def test_superuser_change_fields(self):
        self.request.user = self.superuser
        self.assertEqual(
            tuple(self.model_admin.get_fields(self.request, self.test_user)),
            ("mobile", "password"),
        )

    def test_superuser_exclude_fields(self):
        self.assertEqual(self.model_admin.get_exclude(self.request), None)

    def test_superuser_read_only_fields(self):
        self.assertEqual(self.model_admin.get_readonly_fields(self.request), ())

    def test_superuser_actions(self):
        self.assertEqual(
            tuple(self.model_admin.get_actions(self.request).keys()),
            ("delete_selected",),
        )

    # NOTE ::: These Are example of tests for admin panel in django
    # We're going to follow this. We don't need to test all of them
    # we'll just test attributes that need to be present or change
    # based on user types in the future
