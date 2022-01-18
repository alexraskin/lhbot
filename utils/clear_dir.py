import os


def _clear_dir(directory) -> bool:
	files_in_directory = os.listdir(directory)
	filtered_files = [file for file in files_in_directory if file.endswith(".pdf")]
	for file in filtered_files:
		path_to_file = os.path.join(directory, file)
		os.remove(path_to_file)
	return True