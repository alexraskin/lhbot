import logging
import os
from functools import lru_cache
from typing import Optional, Union

import boto3
from botocore.exceptions import ClientError
from config import Settings
from sentry_sdk import capture_exception


class S3Upload:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.conf = self.settings()
        self.s3_bucket_name = self.conf.s3_bucket_name
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.conf.aws_access_key,
            aws_secret_access_key=self.conf.aws_secret_access_key,
        )

    @lru_cache()
    def settings(self) -> Settings:
        return Settings()

    def upload_file(self, object_name: Optional[str] = None) -> bool:
        if object_name is None:
            object_name = os.path.basename(self.filename)

        try:
            self.client.upload_file(
                f"{self.filename}",
                self.s3_bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
            return False
        return True

    def get_url(self) -> Union[str, bool]:
        try:
            object_url = self.client.generate_presigned_url(
                "get_object",
                ExpiresIn=0,
                Params={"Bucket": self.s3_bucket_name, "Key": self.filename},
            )
            return str(object_url[0 : object_url.index("?")])
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
            return False

    def delete_file(self) -> bool:
        try:
            self.client.delete_object(Bucket=self.s3_bucket_name, Key=self.filename)
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
            return False
        return True
