from django.contrib.auth.models import User
from django.test import override_settings

from tests import PelicanTestCase


class AuthenticationTests(PelicanTestCase):
    def test_anonymous(self):
        self.sign_out()

        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, 403)

    @override_settings(TRUST_REMOTE_USER=False)
    def test_untrusted_header(self):
        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, 403)

    def test_unknown_user(self):
        # Credentials are enough to sign in. The user sees nothing until they are granted a publisher.
        self.sign_in_as("newcomer")

        response = self.client.get("/api/datasets/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.text, [])
        self.assertFalse(User.objects.get(username="newcomer").is_staff)
