from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase


class CreateUserTests(TestCase):
    def test_create(self):
        call_command("createuser", "morgan", "sam")

        for username in ("morgan", "sam"):
            with self.subTest(username=username):
                user = User.objects.get(username=username)
                self.assertFalse(user.is_staff)
                self.assertFalse(user.has_usable_password())

    def test_create_staff(self):
        call_command("createuser", "--staff", "morgan")

        user = User.objects.get(username="morgan")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_promote(self):
        User.objects.create_user("morgan")

        call_command("createuser", "--staff", "morgan")

        user = User.objects.get(username="morgan")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_existing_staff_is_not_demoted(self):
        User.objects.create_user("morgan", is_staff=True)

        call_command("createuser", "morgan")

        self.assertTrue(User.objects.get(username="morgan").is_staff)
