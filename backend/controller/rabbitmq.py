from django.conf import settings
from yapw import clients


class Publisher(clients.Durable, clients.Blocking, clients.Base):
    pass


def publish(*args, **kwargs):
    client = Publisher(url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME)
    try:
        client.publish(*args, **kwargs)
    finally:
        client.close()
