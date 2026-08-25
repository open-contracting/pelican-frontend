import logging

from django.conf import settings
from django.db import connections
from yapw.clients import AsyncConsumer, Blocking
from yapw.decorators import decorate
from yapw.methods import nack

logger = logging.getLogger(__name__)


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


def decorator(decode, callback, state, channel, method, properties, body):
    """
    Close the database connections opened by the callback, before returning.

    If the callback raises an exception, discard the message: requeueing it might upload a duplicate document,
    and shutting down would stop every other export.
    """

    def errback(exception):
        logger.error("Unhandled exception when consuming %r, discarding message", body, exc_info=exception)
        nack(state, channel, method.delivery_tag, requeue=False)

    def finalback():
        for connection in connections.all():
            connection.close()

    decorate(decode, callback, state, channel, method, properties, body, errback, finalback)
