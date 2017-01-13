#!/usr/bin/python

import pika

# http://www.rabbitmq.com/getstarted.html
# http://pika.readthedocs.org/en/latest/modules/parameters.html


def test(username, password, host):
    exchange = 'myexchange'
    vhost = '/'
    routing_key = 'TheQueue'

    credentials = credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, vhost, credentials))
    channel = connection.channel()

    # Create queue

    #### NEEDS DURABLE and other see
    #####https://pastebin.canonical.com/107200/

    channel.queue_declare(queue=routing_key)
    # Create exchange
    channel.exchange_declare(exchange=exchange, type='fanout')
    channel.queue_bind(exchange=exchange, queue=routing_key, routing_key=routing_key)

    channel.basic_publish(exchange=exchange, routing_key=routing_key, body='Hello World! 1')
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body='Hello World! 2')
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body='Hello World! 3')
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return True
