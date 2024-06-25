import argparse
from models.type.prowlarr import Prowlarr
from models.type.radarr import Radarr
from models.type.sonarr import Sonarr

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "create",
        help="Create a backup for the specified server"
    )
    parser.add_argument(
        "servertype",
        choices=["prowlarr", "radarr", "sonarr"],
        help="Type of server to create a backup for"
    )
    parser.set_defaults(func=create_backup)

def create_backup(args):
    server_type = args.servertype

    if server_type == "prowlarr":
        server = Prowlarr()
    elif server_type == "radarr":
        server = Radarr()
    elif server_type == "sonarr":
        server = Sonarr()
    else:
        print(f"⚠️​ Unknown server type: {server_type}")
        return

    server.backup()
