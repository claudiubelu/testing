"""Adds arguments for the Sobolanism CLIs."""


def add_args(parser):
    parser.add_argument(
        "--amqp-host",
        metavar="amqp_host",
        default="localhost",
        type=str,
        help="The AMQP host to connect to.",
    )
