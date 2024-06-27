import logging
import os
from datetime import datetime, timedelta

import boto3


class S3Bucket:
    def __init__(self, endpoint_url, bucket_name, access_key, secret_key):
        self.endpoint_url = endpoint_url
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def list(self, prefix=""):
        objects = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        return objects.get("Contents", [])

    def upload_file(self, file_path, s3_key):
        try:
            self.s3_client.upload_file(
                file_path, self.bucket_name, s3_key, ExtraArgs={"ACL": "private"}
            )
            logging.info(f"File uploaded to S3 successfully as {s3_key}")
            return True
        except Exception as e:
            logging.error(f"Error while uploading {file_path} to S3: {str(e)}")
            return False

    def delete_file(self, path):
        try:
            res = self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)
        except Exception as e:
            logging.error(f"Error while deleting file {path}: {str(e)}")

    def cleanup(self, retention):
        """
        Delete folder older than retention period
        """
        current_time = datetime.utcnow()
        retention_threshold = current_time - timedelta(days=retention)

        for files in self.list():
            obj_datetime = files["LastModified"]
            # Convert obj_datetime to naive datetime for comparison
            obj_datetime_native = obj_datetime.replace(tzinfo=None)

            if obj_datetime_native < retention_threshold:
                self.delete_file(files["Key"])
                
    def file_exists(self, path):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=path)
            return True
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                logging.error(f"Error while checking file existence {path}: {str(e)}")
                return False