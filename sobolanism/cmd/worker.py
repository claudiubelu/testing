"""Console script for sobolanism-worker."""
import argparse
import sys

from sobolanism.cmd import args as cmd_args
from sobolanism.compute import fib
from sobolanism.rpc import worker


def main():
    """Console script for sobolanism-worker."""
    parser = argparse.ArgumentParser()
    cmd_args.add_args(parser)
    args = parser.parse_args()

    print("Arguments: " + str(args.amqp_host))

    svc = fib.FibGenerator()
    w = worker.RPCWorker(svc, "fib-queue2", args.amqp_host)
    w.start_rpc_worker()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
