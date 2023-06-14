#!/usr/bin/env python

"""Tests for `sobolanism.rpc.worker` package."""

import json
import unittest
from unittest import mock

import pika
from pika import channel

from sobolanism.rpc import worker


class TestWorker(unittest.TestCase):
    """Tests for `sobolanism.rpc.worker` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        # Sentinels are just some "values" we don't really care about too much.
        self._worker = worker.RPCWorker(mock.sentinel.svc_obj, mock.sentinel.queue_name)
        self._worker._conn = mock.create_autospec(pika.BlockingConnection)
        self._worker._chan = mock.create_autospec(channel.Channel)

    @mock.patch.object(worker.pika, "BasicProperties")
    @mock.patch.object(worker.RPCWorker, "_handle")
    def test_on_request(self, mock_handle, mock_BasicProperties):
        """Test on_request."""
        something = "sobolan, idk"
        mock_handle.return_value = something
        mock_method = mock.Mock()
        mock_props = mock.Mock()

        self._worker.on_request(
            mock.sentinel.ch, mock_method, mock_props, mock.sentinel.body
        )

        mock_BasicProperties.assert_called_once_with(
            correlation_id=mock_props.correlation_id
        )
        expected_body_dict = {"result": something}
        expected_body = json.dumps(expected_body_dict)
        self._worker._chan.basic_publish.assert_called_once_with(
            excange="",
            routing_key=mock_props.reply_to,
            properties=mock_BasicProperties.return_value,
            body=expected_body,
        )
        self._worker._chan.basic_ack.assert_called_once_with(
            delivery_tag=mock_method.delivery_tag
        )

    @mock.patch.object(worker.RPCWorker, "_handle", autospec=True)
    def test_on_request_exc(self, mock_handle):
        """Test on_request exception."""
        exc = Exception("Expected exception")
        mock_handle.side_effect = exc
        mock_method = mock.Mock()
        mock_props = mock.Mock()

        self._worker.on_request(
            mock.sentinel.ch, mock_method, mock_props, mock.sentinel.body
        )

        expected_body_dict = {"error": str(exc)}
        expected_body = json.dumps(expected_body_dict)
        self._worker._chan.basic_publish.assert_called_once_with(
            excange="",
            routing_key=mock_props.reply_to,
            properties=mock.ANY,  # We don't particularly care about the properties given.
            body=expected_body,
        )
