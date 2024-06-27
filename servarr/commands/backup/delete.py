import logging
import os
from pathlib import Path

import yaml

from ...models.destination.s3 import S3Bucket
from ...models.type.prowlarr import Prowlarr
from ...models.type.radarr import Radarr
from ...models.type.sonarr import Sonarr


# Configure logging
logger = logging.getLogger(__name__)

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "delete",
        help="Delete backups"
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Name of the backup file to delete"
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Delete the latest backup"
    )
    parser.add_argument(
        "--retention",
        action="store_true",
        help="Delete backups older than the retention period"
    )

    parser.set_defaults(func=delete_backup)

    return parser

def delete_backup(args):
    config_dir = os.path.join(Path.home(), ".config", "servarr")
    config_path = os.path.join(config_dir, "config.yml")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run 'servarr config init' first.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    backups = config.get("backups", {})
    starrs = backups.get("starrs", {})
    s3_config = config.get("backups", {}).get("destination", {}).get("s3", {})
    instances_to_check = []
    
    if args.type:
        for service_type in args.type:
            instances = starrs.get(service_type, [])
            if args.instance:
                for instance in instances:
                    if instance['name'] in args.instance or instance['url'] in args.instance:
                        instances_to_check.append((service_type, instance))
            else:
                for instance in instances:
                    instances_to_check.append((service_type, instance))
    else:
        for service_type, instances in starrs.items():
            if args.instance:
                for instance in instances:
                    if instance['name'] in args.instance or instance['url'] in args.instance:
                        instances_to_check.append((service_type, instance))
            else:
                for instance in instances:
                    instances_to_check.append((service_type, instance))
                    
    if not instances_to_check:
        logger.info("No matching instances found. Please check the instance names or URLs specified.")
        return
    
    if args.name:
        s3_bucket = S3Bucket(
            s3_config.get('endpoint'),
            s3_config.get('bucket'),
            s3_config.get('key', {}).get('access'),
            s3_config.get('key', {}).get('secret')
        )
        
        found = False
        for backup in s3_bucket.list():
            if args.name in backup["Key"]:
                found = True
                logger.info(f"Deleting backup '{args.name}' from S3.")
                try:
                    s3_bucket.delete_file(backup["Key"])
                except Exception as e:
                    logger.error(f"Failed to delete backup '{args.name}' from S3: {e}")
        
        if not found:
            logger.info(f"No backups found named: {args.name}")

    elif args.latest:
        for service_type, instance in instances_to_check:
            server_instance = server_instance = get_server_instance(service_type, instance['name'])
            if server_instance:
                latest_backup = server_instance.get_latest_backup()
                if latest_backup:
                    success = server_instance.delete_backup(latest_backup['Key'])
            else:
                logger.info(f"Unknown service type: {service_type}")
    elif args.retention:
        retention_days = int(backups.get("retention", "90d").strip("d"))
        for service_type, instance in instances_to_check:
            server_instance = get_server_instance(service_type, instance['name'])
            if server_instance:
                server_instance.delete_old_backups(retention_days)
    else:
        print("Please specify a backup name, --latest, or --retention.")
        
def get_server_instance(service_type, instance_name):
    if service_type == 'prowlarr':
        return Prowlarr(instance_name)
    elif service_type == 'radarr':
        return Radarr(instance_name)
    elif service_type == 'sonarr':
        return Sonarr(instance_name)
    else:
        return None