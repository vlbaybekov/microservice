#!/usr/bin/env python

import pika, random, time, sys

def main ():
  
    connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.2'))

    channel = connection.channel()

    channel.queue_declare(queue='hello')
    while True:
        randomNumber = random.randint(1000, 10000000)
        channel.basic_publish(exchange='', routing_key='hello', body=str(randomNumber))
        print(" [x] Sent", randomNumber)
        time.sleep(10)

if __name__ == '__main__':
    try:
         main()
    except KeyboardInterrupt:
        print('Interruped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

