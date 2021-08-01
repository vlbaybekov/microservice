#!/usr/bin/env python
import pika, sys, os, datetime, psycopg2

def main():
    connection_rabbit = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection_rabbit.channel()

    channel.queue_declare(queue='hello')

    connection_pg = psycopg2.connect(user = 'pudge',
                                      password = 'pudge',
                                      host = '172.17.0.5',
                                      port = '5432',
                                      database = 'pudge')
    print(connection_pg.get_dsn_parameters(), "\n")
    def callback(ch, method, properties, body):

        print(" [x] Received %r" % body)

        cur = connection_pg.cursor()

        now = datetime.datetime.now()
        print(type(now))
        time = now.strftime("%d-%m-%y %H:%M:%S")
        time = datetime.datetime.strptime(time, '%d-%m-%y %H:%M:%S')
        cur.execute("""INSERT INTO rabbitmq1_logs (timestamp, number) VALUES(%s,%s)""", (time, int(body)))
        connection_pg.commit()
    channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        connection_pg.close()
        cur.close()
        print('Interruped')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
