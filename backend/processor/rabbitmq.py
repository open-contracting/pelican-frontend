from urllib.parse import parse_qs, urlencode, urlsplit

import pika
from django.conf import settings

global connected
connected = False


def publish(message, routing_key):
    if not connected:
        connect()

    channel.basic_publish(
        exchange=settings.RABBIT_EXCHANGE_NAME,
        routing_key=f"{settings.RABBIT_EXCHANGE_NAME}_{routing_key}",
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )


def connect():
    parsed = urlsplit(settings.RABBIT_URL)
    query = parse_qs(parsed.query)
    # NOTE: Heartbeat should not be disabled.
    # https://github.com/open-contracting/data-registry/issues/140
    query.update({"blocked_connection_timeout": 1800, "heartbeat": 0})

    connection = pika.BlockingConnection(pika.URLParameters(parsed._replace(query=urlencode(query)).geturl()))

    global channel
    channel = connection.channel()
    channel.exchange_declare(exchange=settings.RABBIT_EXCHANGE_NAME, durable=True, exchange_type="direct")

    global connected
    connected = True
