import os
import yaml
from pathlib import Path

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "show",
        help="Show current configuration"
    )
    parser.set_defaults(func=show_config)

def show_config(args):
    config_dir = os.path.join(Path.home(), ".config", "servarr")
    config_path = os.path.join(config_dir, "config.yml")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run 'servarr config init' first.")
        return

    with open(config_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)

    print("\n📦 Current Configuration:\n")
    
    backups = config_data.get('backups', {})
    
    print(f"🗓 Retention: {backups.get('retention', '❌ Missing')}")
    log_status = "✅ Enabled" if backups.get('log', False) else "❌ Disabled"
    print(f"📝 Logging: {log_status}")
    
    starrs = backups.get('starrs', {})
    print("\n🔧 Starr Services:")
    for service, instances in starrs.items():
        if not instances:
            print(f"  {service.capitalize()}: ❌ No instances configured")
        else:
            print(f"  {service.capitalize()}:")
            for instance in instances:
                url_status = "🌐 URL: " + (instance.get('url') if instance.get('url') else "❌ Missing")
                api_key_status = "🔑 API Key: " + ("<Hidden>" if instance.get('api_key') else "❌ Missing")
                print(f"    - Name: {instance.get('name', '❌ Missing')}")
                print(f"      {url_status}")
                print(f"      {api_key_status}")

    s3 = backups.get('destination', {}).get('s3', {})
    print("\n💾 Backup Configuration (S3):")
    endpoint_status = "🌐 Endpoint: " + (s3.get('endpoint') if s3.get('endpoint') else "❌ Missing")
    bucket_status = "🪣 Bucket: " + (s3.get('bucket') if s3.get('bucket') else "❌ Missing")
    access_key_status = "🔑 Access Key: " + ("<Hidden>" if s3.get('key', {}).get('access') else "❌ Missing")
    secret_key_status = "🔒 Secret Key: " + ("<Hidden>" if s3.get('key', {}).get('secret') else "❌ Missing")
    print(f"  {endpoint_status}")
    print(f"  {bucket_status}")
    print(f"  {access_key_status}")
    print(f"  {secret_key_status}")