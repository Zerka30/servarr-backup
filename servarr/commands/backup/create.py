import logging
import os
from pathlib import Path

import yaml

from ...models.type.prowlarr import Prowlarr
from ...models.type.radarr import Radarr
from ...models.type.sonarr import Sonarr


# Configure logging
logger = logging.getLogger(__name__)

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "create",
        help="Create backups"
    )
    parser.set_defaults(func=create_backup)
    
    return parser

def create_backup(args):
    config_dir = os.path.join(Path.home(), ".config", "servarr")
    config_path = os.path.join(config_dir, "config.yml")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run 'servarr config init' first.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    backups = config.get("backups", {})
    starrs = backups.get("starrs", {})
    destination = backups.get("destination", {}).get("s3", {})

    instances_to_backup = []

    if args.type:
        for service_type in args.type:
            instances = starrs.get(service_type, [])
            if args.instance:
                for instance in instances:
                    if instance['name'] in args.instance or instance['url'] in args.instance:
                        instances_to_backup.append((service_type, instance))
            else:
                for instance in instances:
                    instances_to_backup.append((service_type, instance))
    else:
        for service_type, instances in starrs.items():
            if args.instance:
                for instance in instances:
                    if instance['name'] in args.instance or instance['url'] in args.instance:
                        instances_to_backup.append((service_type, instance))
            else:
                for instance in instances:
                    instances_to_backup.append((service_type, instance))

    if not instances_to_backup:
        logger.info("No matching instances found. Please check the instance names or URLs specified.")
        return

    for service_type, instance in instances_to_backup:
        if service_type == 'prowlarr':
            prowlarr = Prowlarr(instance['name'])
            prowlarr.backup()
        elif service_type == 'radarr':
            radarr = Radarr(instance['name'])
            radarr.backup()
        elif service_type == 'sonarr':
            sonarr = Sonarr(instance['name'])
            sonarr.backup()
        else:
            print(f"Unknown service type: {service_type}")
