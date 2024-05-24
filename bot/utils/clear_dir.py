import os

from sentry_sdk import capture_exception


def clean_cache(directory: str, ext: str) -> bool:
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(ext)]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        try:
            os.remove(path_to_file)
        except Exception as e:
            capture_exception(e)
            return False
    return True
