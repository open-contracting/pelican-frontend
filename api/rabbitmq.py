from functools import partial

from django.conf import settings
from django.db import close_old_connections
from yapw.clients import AsyncConsumer, Blocking
from yapw.decorators import discard


def publish(*args, **kwargs):
    client = Blocking(url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME)
    try:
        client.publish(*args, **kwargs)
    finally:
        client.close()


def consume(*args, **kwargs):
    """Consume messages from RabbitMQ."""
    client = AsyncConsumer(*args, url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME, **kwargs)
    client.start()


# Django closes old connections between requests. A consumer similarly needs to close old connections between messages.
close_old_connections_and_discard = partial(discard, finalback=close_old_connections)
