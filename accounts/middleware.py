from django.conf import settings
from django.contrib.auth import middleware

from accounts.authentication import HEADER


class RemoteUserMiddleware(middleware.RemoteUserMiddleware):
    """Sign in the user for the Django administration site. REST Framework's authentication runs only in API views."""

    header = HEADER

    def process_request(self, request):
        if settings.TRUST_REMOTE_USER:
            super().process_request(request)
