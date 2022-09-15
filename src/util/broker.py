import pika
import json

from src.config import BROKER_URL


def declare_queue():
    """
    Declare the queue
    """

    # Create a new connection to the broker
    connection = pika.BlockingConnection(pika.URLParameters(BROKER_URL))

    # Create a new channel
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue="cuts", durable=True)

    # Close the connection
    connection.close()


def send_cuts(cuts: list):
    """
    Send cuts to the broker
    """

    # Create a new connection to the broker
    connection = pika.BlockingConnection(pika.URLParameters(BROKER_URL))

    # Create a new channel
    channel = connection.channel()

    # Send the cuts to the queue
    channel.basic_publish(exchange="", routing_key="cuts", body=json.dumps(cuts))

    # Close the connection
    connection.close()
