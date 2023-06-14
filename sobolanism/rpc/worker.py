import json
import logging

import pika

from sobolanism import exception as exc


LOG = logging.getLogger(__name__)


class RPCWorker:
    def __init__(self, svc, queue_name, host="localhost"):
        self._svc = svc
        self._queue_name = queue_name
        self._host = host
        self._conn = None
        self._chan = None

    def start_rpc_worker(self):
        params = pika.ConnectionParameters(host=self._host)
        self._conn = pika.BlockingConnection(params)
        self._chan = self._conn.channel()
        self._chan.queue_declare(queue=self._queue_name)

        self._chan.basic_qos(prefetch_count=1)
        self._chan.basic_consume(
            queue=self._queue_name, on_message_callback=self.on_request
        )

        # This is a blocking call.
        self._chan.start_consuming()

    def on_request(self, ch, method, props, body):
        LOG.info("Got a request...: %s, %s, %s", method, props, body)
        result = {}
        try:
            result["result"] = self._handle(body)
        except Exception as ex:
            # Marshall the error and send it back to the caller.
            result["error"] = str(ex)

        # Send the reply back to the original caller.
        reply_props = pika.BasicProperties(correlation_id=props.correlation_id)
        self._chan.basic_publish(
            excange="",
            routing_key=props.reply_to,
            properties=reply_props,
            body=json.dumps(result),
        )
        self._chan.basic_ack(delivery_tag=method.delivery_tag)

    def _handle(self, body):
        data = json.loads(body)

        LOG.info("Received call: %s", data)

        method_name = data.get("method_name")
        if not method_name:
            raise exc.InvalidRPCMethod(method_name=method_name)

        method = getattr(self._svc, method_name, None)
        if method is None or not callable(method):
            raise exc.InvalidRPCMethod(method_name=method_name)

        args = data.get("args", [])
        kvargs = data.get("kvargs", {})
        return method(*args, **kvargs)
