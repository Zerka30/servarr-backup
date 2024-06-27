import os
import yaml
from pathlib import Path
import argparse

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "init",
        help="Initialize configuration"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Generate a default configuration file without interactive prompts"
    )
    parser.set_defaults(func=init_config)

def init_config(args):  # Accept an argument to avoid the TypeError
    config_dir = os.path.join(Path.home(), ".config", "servarr")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.yml")

    if args.non_interactive:
        config_data = {
            'backups': {
                'retention': '90d',
                'log': True,
                'starrs': {
                    'lidarr': [],
                    'radarr': [{
                            'name': 'example',
                            'url': 'https://sonarr.domain.tld',
                            'api_key': ''
                        }],
                    'readarr': [],
                    'sonarr': [],
                    'prowlarr': []
                },
                'destination': {
                    's3': {
                        'endpoint': 'https://s3.pub1.infomaniak.cloud',
                        'bucket': 'servarr',
                        'key': {
                            'access': '',
                            'secret': ''
                        }
                    }
                }
            }
        }
    else:
        config_data = {
            'backups': {
                'retention': input("Enter retention period (e.g., 90d): "),
                'log': True if input("Enable logging? (y/n): ").lower() == 'y' else False,
                'starrs': {},
                'destination': {
                    's3': {
                        'endpoint': input("Enter S3 endpoint: "),
                        'bucket': input("Enter S3 bucket name: "),
                        'key': {
                            'access': input("Enter S3 access key: "),
                            'secret': input("Enter S3 secret key: ")
                        }
                    }
                }
            }
        }

        starr_services = ['lidarr', 'radarr', 'readarr', 'sonarr', 'prowlarr']
        for service in starr_services:
            instances = []
            add_instance = input(f"Add instance for {service}? (y/n): ").lower() == 'y'
            while add_instance:
                instance = {
                    'name': input(f"Enter name for {service} instance: "),
                    'url': input(f"Enter URL for {service} instance: "),
                    'api_key': input(f"Enter API key for {service} instance: ")
                }
                instances.append(instance)
                add_instance = input(f"Add another instance for {service}? (y/n): ").lower() == 'y'
            if instances:
                config_data['backups']['starrs'][service] = instances

    with open(config_path, 'w') as config_file:
        yaml.dump(config_data, config_file, sort_keys=False)

    print(f"Configuration initialized and saved to {config_path}")