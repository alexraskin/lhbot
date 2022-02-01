import os


def _clear_dir(directory: str, ext: str) -> bool:
    """
    The _clear_dir function specifically clears the directory of all files with
    the specified extension.

    :param directory:str: Used to specify the directory that is to be cleared.
    :param ext:str: Used to specify the file extension to filter for.
    :return: a boolean value that tells us whether the directory was successfully cleared.

    """
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(ext)]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    return True
