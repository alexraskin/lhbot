from functools import lru_cache

from config import Settings
from filestack import Client


@lru_cache()
def settings():
    return Settings()


conf = settings()


class FileSharer:
    def __init__(self, filepath: str, api_key: str = conf.filestack_api_key):
        """
        The __init__ function is the constructor for a class. It sets up or "initializes" the object.

        :param self: Used to refer to the object itself.
        :param filepath: Used to store the path of the file that is uploaded.
        :param api_key=config["filestack_key"]: Used to set the api key for the filepicker.
        :return: the instantiation of the class, in this case an instance of the Filelink class.

        """
        self.filepath = filepath
        self.api_key = api_key

    def share(self) -> str:
        """
        The share function creates a new filelink object that is then used to share the file with other users.
        The function takes in the api key and uses it to create a client object, which is then used to create a new
        filelink object. The link of this newly created filelink is returned.

        :param self: Used to access the attributes and methods of the class in python.
        :return: the share link.

        """
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
