from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(mobile="+201010092181", password="foo")
        self.assertEqual(user.mobile, "+201010092181")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        self.assertTrue(user.check_password("foo"))
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(mobile="")
        with self.assertRaises(TypeError):
            User.objects.create_user(password="")
        with self.assertRaises(ValidationError):
            User.objects.create_user(mobile="123", password="foo")
        with self.assertRaises(ValidationError):
            User.objects.create_user(mobile="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("+201010092181", "foo")
        self.assertEqual(admin_user.mobile, "+201010092181")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                mobile="+201010092181", password="foo", is_superuser=False
            )
