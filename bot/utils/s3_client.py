import logging
import os
from functools import lru_cache
from typing import Optional, Union

import boto3
from botocore.exceptions import ClientError
from config import Settings
from sentry_sdk import capture_exception


class S3Upload:
    """
    S3Upload is a class that contains all the methods to upload,
    delete and get a presigned url for a file.
    Parameters:
    filename: str: The name of the file to upload
    """

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
        """
        The settings function is a property that returns the Settings object.
        It's a convenience function to make it easy to access the settings without
        having to import them everywhere.  This way, we can use the settings in places
        where we don't want/need to use an entire module.

        :param self: Access variables that belongs to the class
        :return: An instance of the settings class
        """
        return Settings()

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
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
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
            return str(object_url[0 : object_url.index("?")])
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
            return False

    def delete_file(self) -> bool:
        """
        The delete_file function deletes a file from an S3 bucket.

        :param self: Access variables that belongs to the class
        :return: Boolean value if the file was deleted or not
        """
        try:
            self.client.delete_object(Bucket=self.s3_bucket_name, Key=self.filename)
        except ClientError as error:
            logging.error(error)
            capture_exception(error)
            return False
        return True
