import argparse
from models.type.prowlarr import Prowlarr
from models.type.radarr import Radarr
from models.type.sonarr import Sonarr

import humanize
from datetime import datetime
from tabulate import tabulate

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "ls",
        help="List backups for the specified server"
    )
    parser.add_argument(
        "servertype",
        choices=["prowlarr", "radarr", "sonarr"],
        help="Type of server to list backups for"
    )
    parser.set_defaults(func=list_backups)

def list_backups(args):
    server_type = args.servertype

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
        backups = server.list_backups()
        if not backups:
            print("No backups found.")
            return

        table = []
        for backup in backups:
            last_modified = backup['LastModified']
            if isinstance(last_modified, str):
                last_modified = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%f%z")
            formatted_date = last_modified.strftime("%Y-%m-%d %H:%M:%S")
            size = humanize.naturalsize(backup['Size'], binary=True)
            table.append([backup['Key'], formatted_date, size])
        print(tabulate(table, headers=["Key", "Date", "Size"], tablefmt="grid"))
    except Exception as e:
        print(f"Error: {e}")
