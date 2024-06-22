import os
import json

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "init",
        help="Initialize configuration"
    )
    parser.set_defaults(func=init_config)

def init_config(args):
    config = {
        "starrs":  {
            "lidarr": {
                "url": "",
                "api_key": ""
            },
            "radarr": {
                "url": input("Enter Radarr URL: "),
                "api_key": input("Enter Radarr API Key: ")
            },
            "readarr": {
                "url": "",
                "api_key": ""
            },
            "sonarr": {
                "url": input("Enter Sonarr URL: "),
                "api_key": input("Enter Sonarr API Key: ")
            },
            "prowlarr": {
                "url": input("Enter Prowlarr URL: "),
                "api_key": input("Enter Prowlarr API Key: ")
            }
        },
        "backup": {
            "s3": {
                "endpoint": input("Enter S3 Endpoint: "),
                "bucket": input("Enter S3 Bucket: "),
                "key": {
                    "access": input("Enter S3 Access Key: "),
                    "secret": input("Enter S3 Secret Key: ")
                }
            }
        }
    }
                
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "servarr")
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, "config.json")

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    print(f"Configuration initialized and saved to {config_path}")
