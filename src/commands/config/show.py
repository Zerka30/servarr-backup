import os
import json

def add_subparser(subparsers):
    parser = subparsers.add_parser(
        "show",
        help="Show current configuration"
    )
    parser.set_defaults(func=show_config)

def show_config(args):
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "servarr")
    config_path = os.path.join(config_dir, "config.json")

    if not os.path.exists(config_path):
        print("❌ Configuration file not found. Please run 'servarr config init' first.")
        return

    with open(config_path, 'r') as f:
        config = json.load(f)

    starrs = config.get("starrs", {})
    backup = config.get("backup", {}).get("s3", {})

    print("\n📦 Current Configuration:\n")
    print("🔧 Starr Services:")
    for service, details in starrs.items():
        url_status = "🌐 URL: " + (details.get('url') if details.get('url') else "❌ Missing")
        api_key_status = "🔑 API Key: " + ("<Hidden>" if details.get('api_key') else "❌ Missing")
        print(f"  {service.capitalize()}:")
        print(f"    {url_status}")
        print(f"    {api_key_status}")

    print("\n💾 Backup Configuration (S3):")
    endpoint_status = "🌐 Endpoint: " + (backup.get('endpoint') if backup.get('endpoint') else "❌ Missing")
    bucket_status = "🪣 Bucket: " + (backup.get('bucket') if backup.get('bucket') else "❌ Missing")
    access_key_status = "🔑 Access Key: " + ("<Hidden>" if backup.get('key', {}).get('access') else "❌ Missing")
    secret_key_status = "🔒 Secret Key: " + ("<Hidden>" if backup.get('key', {}).get('secret') else "❌ Missing")
    print(f"  {endpoint_status}")
    print(f"  {bucket_status}")
    print(f"  {access_key_status}")
    print(f"  {secret_key_status}")

    print("\n")
