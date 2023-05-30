import json
import logging
import uuid

import pika

from sobolanism import exception as exc


LOG = logging.getLogger(__name__)


class RPCClient:
    def __init__(self, queue_name, host="localhost"):
        self._queue_name = queue_name
        self._host = host

        # Open an exclusive channel for callbacks / replies.
        params = pika.ConnectionParameters(host=host)
        self._conn = pika.BlockingConnection(params)
        self._chan = self._conn.channel()
        result = self._chan.queue_declare(queue="", exclusive=True)
        self._callback_queue = result.method.queue

        self._chan.basic_consume(
            queue=self._callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True,
        )

        self._result = None
        self._corr_id = None

    def _on_response(self, ch, method, props, body):
        if self._corr_id != props.correlation_id:
            return

        LOG.info("Got a response. method=%s, props=%s, body=%s", method, props, body)

        # Process the response.
        try:
            response = json.loads(body)
            if "error" in response:
                raise exc.SobolanRPCException(response["error"])

            self._result = response.get("result")
        except Exception as ex:
            LOG.error(ex)
            raise exc.SobolanRPCException(ex)

    def call(self, method_name, *args, **kvargs):
        self._result = None
        self._corr_id = str(uuid.uuid4())
        props = pika.BasicProperties(
            reply_to=self._callback_queue, correlation_id=self._corr_id
        )
        body = {"method_name": method_name, "args": args, "kvargs": kvargs}

        self._chan.basic_publish(
            exchange="",
            routing_key=self._queue_name,
            properties=props,
            body=json.dumps(body),
        )

        LOG.info("Waiting for a response...")
        self._conn.process_data_events(time_limit=None)
        LOG.info("Finished waiting for a response...")
        return self._result
