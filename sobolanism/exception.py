"""Sobolanism base exception handling."""

import logging

LOG = logging.getLogger(__name__)


class SobolanismException(Exception):
    """Base Sobolanism Exception

    To correctly use this class, inherit from it and define the "msg_fmt"
    property, which will then be string formatted with the keyword arguments
    given in the constructor.
    """

    msg_fmt = "An unknown exception occured"

    def __init__(self, message=None, **kwargs):
        try:
            if not message:
                message = self.msg_fmt % kwargs
            else:
                message = str(message)
        except Exception as ex:
            LOG.exception(
                "Exception in string format operation: "
                "Exc: %s, msg_fmt: %s, kwargs: %s",
                ex,
                self.msg_fmt,
                kwargs,
            )
            message = self.msg_fmt

        super().__init__(message)


class InvalidRPCMethod(SobolanismException):
    msg_fmt = "The RPC Method call '%(method_name)s' is invalid."


class SobolanRPCException(SobolanismException):
    pass
