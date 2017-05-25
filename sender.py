import rpc_utils


connection, channel = rpc_utils.create_connection(
    'localhost', 'stackrabbit', 'Passw0rd')
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

