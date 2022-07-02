import os
from functools import lru_cache
from typing import Union, Optional

import boto3
import botocore
from botocore.exceptions import ClientError
from config import Settings
from sentry_sdk import capture_exception


@lru_cache()
def settings():
    return Settings()


conf = settings()


class S3Upload:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.s3_bucket_name = conf.s3_bucket_name
        self.config = botocore.client.Config(signature_version=botocore.UNSIGNED)
        self.client = boto3.client(
            "s3",
            aws_access_key_id=conf.aws_access_key,
            aws_secret_access_key=conf.aws_secret_access_key,
            config=self.config,
        )

    def upload_file(self, object_name: Optional[str] = None) -> bool:
        """
        The upload_file function uploads a file to an S3 bucket.
        :param self: Access the attributes and methods of the class in python
        :return: Boolean value if the file was uploaded or not
        """
        if object_name is None:
            object_name = os.path.basename(self.filename)

        try:
            self.client.upload_file(
                f"{self.filename}",
                self.s3_bucket_name,
                object_name,
                ExtraArgs={"ACL": "public-read"},
            )
        except ClientError as e:
            capture_exception(e)
            return False
        return True

    def get_url(self) -> Union[str, bool]:
        """
        The get_url function returns a presigned URL for the S3 object.

        :param self: Access variables that belongs to the class
        :return: A presigned url to access the file from s3 or False if there was an error
        """
        try:
            object_url = self.client.generate_presigned_url(
                "get_object",
                ExpiresIn=0,
                Params={"Bucket": self.s3_bucket_name, "Key": self.filename},
            )
            return str(object_url)
        except ClientError as e:
            capture_exception(e)
            return False
