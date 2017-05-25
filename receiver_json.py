from testing import rpcapi


endpoint = rpcapi.HelloRPCEndpoint()
endpoint.start_consuming()

"""
connection, channel = rpc_utils.create_connection(
    'localhost', 'stackrabbit', 'Passw0rd')
channel.queue_declare(queue='hello')

class RPCEndpoint(object):

    def hello(self, foo, bar):
        print "Heya! Got an RPC call..."
        print "foo='%(foo)s' bar='%(bar)s'" % dict(foo=foo, bar=bar)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        message = json.loads(body)
        method = message.get('method')

        if not method or method not in self.__dict__.keys():
            print "received bad method name: %s" % method

        args = message.get('args', [])
        kwargs = message.get('kwargs', {})

        getattr(self, method)(*args, **kwargs)


endpoint = RPCEndpoint()

channel.basic_consume(endpoint.callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
"""
