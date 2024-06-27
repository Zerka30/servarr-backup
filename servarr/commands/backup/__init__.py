from . import create, delete, ls


def add_subparser(subparsers):
    backup_parser = subparsers.add_parser(
        "backup",
        help="Backup commands"
    )

    backup_subparsers = backup_parser.add_subparsers(
        title="Backup commands", dest="subcommand"
    )

    # Add subparsers for each subcommand
    create_parser = create.add_subparser(backup_subparsers)
    delete_parser = delete.add_subparser(backup_subparsers)
    ls_parser = ls.add_subparser(backup_subparsers)

    # Add common arguments to all backup subcommands
    for p in [create_parser, delete_parser, ls_parser]:
        p.add_argument(
            "--instance",
            action="append",
            help="Specify an instance by name or URL"
        )
        p.add_argument(
            "--type",
            action="append",
            choices=["prowlarr", "radarr", "sonarr"],
            help="Specify the type of servers"
        )

    # Default action when no subcommand is provided
    backup_parser.set_defaults(func=lambda args: backup_parser.print_help())
