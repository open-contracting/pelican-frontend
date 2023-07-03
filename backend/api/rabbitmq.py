from django.conf import settings
from yapw.clients import Blocking


def publish(*args, **kwargs):
    client = Blocking(url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME)
    try:
        client.publish(*args, **kwargs)
    finally:
        client.close()
