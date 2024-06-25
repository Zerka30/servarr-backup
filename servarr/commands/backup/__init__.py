from . import create
from . import delete
from . import ls

def add_subparser(subparsers):
    backup_parser = subparsers.add_parser(
        "backup",
        help="Backup commands"
    )
    
    backup_subparsers = backup_parser.add_subparsers(
        title="Backup commands", dest="subcommand"
    )

    # Add subparsers for each subcommand
    create.add_subparser(backup_subparsers)
    delete.add_subparser(backup_subparsers)
    ls.add_subparser(backup_subparsers)
    
    # Default action when no subcommand is provided
    backup_parser.set_defaults(func=lambda args: backup_parser.print_help())
