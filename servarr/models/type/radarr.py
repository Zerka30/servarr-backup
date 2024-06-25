import os
import json
import requests
import time
import logging
from . import Server
from ..destination.s3 import S3Bucket


# Configure logging
logger = logging.getLogger(__name__)


class Radarr(Server):
    def __init__(self):
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "servarr")
        config_path = os.path.join(config_dir, "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError("Configuration file not found. Please run 'servarr config init' first.")

        with open(config_path, 'r') as f:
            config = json.load(f)

        radarr_config = config.get("starrs", {}).get("radarr", {})
        s3_config = config.get("backup", {}).get("s3", {})
        url = radarr_config.get("url")
        api_key = radarr_config.get("api_key")

        if not url or not api_key:
            raise ValueError("Radarr URL or API Key is missing in the configuration.")

        super().__init__(url, api_key)

        self.s3_bucket = S3Bucket(
            s3_config.get('endpoint'),
            s3_config.get('bucket'),
            s3_config.get('key', {}).get('access'),
            s3_config.get('key', {}).get('secret')
        )

    def backup(self):
        # Create Backup
        self.create_backup()
        
        # Download Backup
        backup_path = self.download_latest_backup()
        
        if backup_path:
            # Upload Backup to S3
            s3_key = os.path.basename(backup_path)
            upload_success = self.s3_bucket.upload_file(backup_path, f"radarr/{s3_key}")
            
            if upload_success:
                # Delete Backup from local file system
                os.remove(backup_path)
                logger.info(f"Deleted local backup file {backup_path} successfully.")
                
                # Delete Backup from Radarr server
                backup_id = self.get_backup_id(s3_key)
                if backup_id:
                    self.delete_backup(backup_id)
                else:
                    logger.error(f"Failed to retrieve backup ID for {s3_key}.")


    def create_backup(self):
        url = f"{self.url}/api/v3/command"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
        logger.info("Starting backup creation for Radarr.")
        logger.debug(f"Requesting URL: {url}")
        logger.debug(f"Using headers: {headers}")
        
        res = requests.post(url, headers=headers, json={"name": "Backup"})
        
        if res.status_code == 201:
            command_id = res.json().get('id')
            self.backup_id = command_id
            logger.info(f"Created backup command successfully with ID: {command_id}")
            if command_id:
                if self.wait_for_completion(command_id):
                    logger.info("Completed backup for Radarr successfully.")
                else:
                    logger.error("Failed to complete backup for Radarr.")
            else:
                logger.error("Failed to retrieve command ID for backup creation.")
        else:
            logger.error(f"Failed to create backup for Radarr. Status code: {res.status_code}")
            logger.debug(f"Response body: {res.text}")


    def delete_backup(self, backup_name):
        logger.info(f"Deleting backup '{backup_name}' from S3 for Radarr.")
        try:
            self.s3_bucket.delete_file(f"radarr/{backup_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete backup '{backup_name}' from S3: {e}")
            return False


    def list_backups(self):
        return self.s3_bucket.list("radarr")


    def download_latest_backup(self):
        url = f"{self.url}/api/v3/system/backup"
        headers = {
            "X-Api-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info("Downloading the latest backup.")
        res = requests.get(url, headers=headers)
        
        if res.status_code != 200:
            logger.error(f"Failed to retrieve backups. Status code: {res.status_code}")
            return None
        
        backups = res.json()
        manual_backup = next((b for b in backups if b.get('type') == 'manual'), None)

        if not manual_backup or not manual_backup.get('path'):
            logger.error("No recent manual backup found.")
            return None

        backup_path = manual_backup['path']
        download_url = f"{self.url}{backup_path}"
        logger.debug(f"Downloading backup from URL: {download_url}")
        backup_res = requests.get(download_url, headers=headers)

        if backup_res.status_code == 200:
            backup_file_path = os.path.join("/tmp", os.path.basename(backup_path))
            with open(backup_file_path, 'wb') as f:
                f.write(backup_res.content)
            logger.info(f"Downloaded backup successfully to {backup_file_path}")
            return backup_file_path
        else:
            logger.error(f"Failed to download the backup. Status code: {backup_res.status_code}")
            return None


    def get_backup_id(self, backup_name):
        url = f"{self.url}/api/v3/system/backup"
        headers = {
            "X-Api-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info(f"Retrieving backup ID for {backup_name}.")
        res = requests.get(url, headers=headers)
        
        if res.status_code != 200:
            logger.error(f"Failed to retrieve backups. Status code: {res.status_code}")
            return None
        
        backups = res.json()
        backup = next((b for b in backups if b.get('name') == backup_name), None)

        if backup:
            return backup.get('id')
        else:
            logger.error(f"Backup {backup_name} not found.")
            return None


    def wait_for_completion(self, command_id):
        url = f"{self.url}/api/v3/command/{command_id}"
        headers = {
            "X-Api-Key": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        logger.info(f"Waiting for completion of backup command ID: {command_id}")
        while True:
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                logger.error(f"Failed to retrieve command status. Status code: {res.status_code}")
                return False

            command_status = res.json().get('status')
            logger.debug(f"Command status: {command_status}")
            if command_status == 'completed':
                return True
            time.sleep(1)  # Wait for 1 second before the next status check