import rpc_utils


connection, channel = rpc_utils.create_connection(
    'localhost', 'stackrabbit', 'Passw0rd')
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    import pdb; pdb.set_trace()
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

