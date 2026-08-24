"""
How a request is authenticated.

Authenticate the request in a proxy, and set the ``X-Remote-User`` header to the username. Set the
``DJANGO_PROXY`` environment variable, so that Django trusts the header. Otherwise, every request 403's.

Django checks no password. It creates the user on their first request, who sees no datasets until they are
granted a publisher, or promoted to staff.
"""

from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication

HEADER = "HTTP_X_REMOTE_USER"


class RemoteUserAuthentication(authentication.RemoteUserAuthentication):
    """
    Authenticate the request's user.

    No CSRF token is sent, and no CSRF check runs. Instead, a cross-site write is stopped by the JSON-only
    ``DEFAULT_PARSER_CLASSES`` (which no HTML form satisfies) and by CORS in production.
    """

    header = HEADER

    def authenticate(self, request):
        if not settings.TRUST_REMOTE_USER:
            return None
        return super().authenticate(request)


class RemoteUserAuthenticationExtension(OpenApiAuthenticationExtension):
    """
    Declare the security scheme for this class in the OpenAPI document.

    drf-spectacular declares security schemes only for REST Framework's authentication classes. Declare the credentials
    that the client sends, except the ``X-Remote-User`` header, which the proxy unsets before reaching Django.

    https://drf-spectacular.readthedocs.io/en/latest/customization.html#specify-authentication-with-openapiauthenticationextension
    """

    target_class = RemoteUserAuthentication
    name = "basicAuth"

    def get_security_definition(self, auto_schema):  # noqa: ARG002
        return {"type": "http", "scheme": "basic"}
