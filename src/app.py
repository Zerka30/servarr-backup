import argparse
import config as cfg

import commands.config as config
import commands.backup as backup

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(message)s",
)


def main():
    parser = argparse.ArgumentParser(description="Mediabox Backup Tool", prog="servarr")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="Servarr v" + cfg.VERSION,
        help="show servarr version",
    )

    config.add_subparser(subparsers)
    backup.add_subparser(subparsers)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
