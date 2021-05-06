
import pika
from django.conf import settings

global connected
connected = False


def publish(message, routing_key):
    if not connected:
        connect()

    channel.basic_publish(
        exchange=settings.RABBIT["exchange_name"],
        routing_key=settings.RABBIT["exchange_name"] + routing_key,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )


def connect():
    credentials = pika.PlainCredentials(settings.RABBIT["username"], settings.RABBIT["password"])

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBIT["host"],
        port=settings.RABBIT["port"],
        credentials=credentials,
        blocked_connection_timeout=1800,
        heartbeat=0
    ))

    global channel
    channel = connection.channel()
    channel.exchange_declare(
        exchange=settings.RABBIT["exchange_name"],
        durable='true',
        exchange_type='direct'
    )

    global connected
    connected = True
