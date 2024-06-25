from . import init
from . import show

def add_subparser(subparsers):
    config_parser = subparsers.add_parser(
        "config",
        aliases=["cfg", "conf"],
        help="Manage config"
    )
    
    config_subparsers = config_parser.add_subparsers(
        title="Configuration commands", dest="subcommand"
    )

    # Add subparsers for each subcommand
    init.add_subparser(config_subparsers)
    show.add_subparser(config_subparsers)

    # Default action when no subcommand is provided
    config_parser.set_defaults(func=lambda args: config_parser.print_help())
