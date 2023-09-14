import os


def clean_cache(directory: str, ext: str) -> bool:
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(ext)]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    return True
