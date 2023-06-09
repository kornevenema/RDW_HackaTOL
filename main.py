#!/usr/bin/env python
import pika
import pandas as pd
from sodapy import Socrata

client = Socrata("opendata.rdw.nl", None)

credentials = pika.PlainCredentials("reader", "reader")
connection = pika.BlockingConnection(
    pika.ConnectionParameters('108.143.79.237',
                              5672,
                              '/',
                              credentials))
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='toll', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

results = client.get("m9d7-ebf2", limit=1, where="kenteken='0001TV'")
