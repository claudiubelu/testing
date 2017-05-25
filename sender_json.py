from testing import rpcapi


hello_api = rpcapi.HelloRPCAPI()
hello_api.hello("lish", bar='tender')
hello_api.close()


"""
connection, channel = rpc_utils.create_connection(
    'localhost', 'stackrabbit', 'Passw0rd')
channel.queue_declare(queue='hello')

message = {
    'method': 'hello',
    'args': ['lish'],
    'kwargs': {'bar': 'tender'}
}

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json.dumps(message))
print(" [x] Sent '%s'" % message)
connection.close()
"""
