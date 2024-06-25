import argparse
from ...models.type.prowlarr import Prowlarr
from ...models.type.radarr import Radarr
from ...models.type.sonarr import Sonarr

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "delete",
        help="Delete a specific backup for the specified server"
    )
    parser.add_argument(
        "servertype",
        choices=["prowlarr", "radarr", "sonarr"],
        help="Type of server to delete the backup from"
    )
    parser.add_argument(
        "backup_name",
        help="Name of the backup file to delete"
    )
    parser.set_defaults(func=delete_backup)

def delete_backup(args):
    server_type = args.servertype
    backup_name = args.backup_name

    if server_type == "prowlarr":
        server = Prowlarr()
    elif server_type == "radarr":
        server = Radarr()
    elif server_type == "sonarr":
        server = Sonarr()
    else:
        print(f"Unknown server type: {server_type}")
        return

    try:
        server.delete_backup(backup_name)
    except Exception as e:
        print(f"Error: {e}")
