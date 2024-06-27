import os
from datetime import datetime
from pathlib import Path

import humanize
import yaml
from tabulate import tabulate

from ...models.type.prowlarr import Prowlarr
from ...models.type.radarr import Radarr
from ...models.type.sonarr import Sonarr


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "ls",
        help="List backups"
    )

    parser.set_defaults(func=list_backups)
    
    return parser

def list_backups(args):
    config_dir = os.path.join(Path.home(), ".config", "servarr")
    config_path = os.path.join(config_dir, "config.yml")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run 'servarr config init' first.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    backups = config.get("backups", {})
    starrs = backups.get("starrs", {})
    
    instances_to_check = []

    if args.instance:
        for service_type, instances in starrs.items():
            for instance in instances:
                if instance['name'] in args.instance or instance['url'] in args.instance:
                    instances_to_check.append((service_type, instance))
        if not instances_to_check:
            print(f"No instances found matching: {args.instance}")
            return
    elif args.type:
        for service_type in args.type:
            instances = starrs.get(service_type, [])
            for instance in instances:
                instances_to_check.append((service_type, instance))
        if not instances_to_check:
            print(f"No instances found for types: {args.type}")
            return
    else:
        for service_type, instances in starrs.items():
            for instance in instances:
                instances_to_check.append((service_type, instance))

    backup_list = []

    for service_type, instance in instances_to_check:
        if service_type == 'prowlarr':
            prowlarr = Prowlarr(instance['name'])
            backups = prowlarr.list_backups()
        elif service_type == 'radarr':
            radarr = Radarr(instance['name'])
            backups = radarr.list_backups()
        elif service_type == 'sonarr':
            sonarr = Sonarr(instance['name'])
            backups = sonarr.list_backups()
        else:
            print(f"Unknown service type: {service_type}")
            continue

        for backup in backups:
            size_humanized = humanize.naturalsize(backup['Size'], binary=True)
            backup_list.append([
                service_type.capitalize(),
                instance['name'],
                backup['Key'],
                backup['LastModified'].strftime("%Y-%m-%d %H:%M:%S"),
                size_humanized
            ])

    if backup_list:
        print(tabulate(
            backup_list,
            headers=["Type", "Instance", "Key", "Date", "Size"],
            tablefmt="pretty",
            colalign=("left", "left", "left", "left", "right")
        ))
    else:
        print("No backups found.")
