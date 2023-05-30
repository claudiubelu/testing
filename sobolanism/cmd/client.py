"""Console script for sobolanism-client."""
import argparse
import sys

from sobolanism.cmd import args as cmd_args
from sobolanism.rpc import fibrpcapi


def main():
    """Console script for sobolanism-client."""
    parser = argparse.ArgumentParser()
    cmd_args.add_args(parser)
    args = parser.parse_args()

    print("Arguments: " + str(args.amqp_host))

    fib = fibrpcapi.FibRPCAPI("fib-queue2", args.amqp_host)
    print(fib.fibonate(10))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
