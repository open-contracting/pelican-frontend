from django.conf import settings
from yapw.clients import AsyncConsumer, Blocking


def publish(*args, **kwargs):
    client = Blocking(url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME)
    try:
        client.publish(*args, **kwargs)
    finally:
        client.close()


def consume(*args, **kwargs):
    """Consume messages, running each callback in a thread, so that a long callback doesn't stop the heartbeat."""
    client = AsyncConsumer(*args, url=settings.RABBIT_URL, exchange=settings.RABBIT_EXCHANGE_NAME, **kwargs)
    client.start()
