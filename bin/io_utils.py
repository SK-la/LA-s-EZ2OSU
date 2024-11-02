#bin/io_utils.py
import pathlib

async def find_duplicate_files(folder_path):
    file_dict = {}
    duplicate_files = []

    for file_path in pathlib.Path(folder_path).rglob('*'):
        if file_path.is_file():
            file_name = file_path.name
            if file_name in file_dict:
                duplicate_files.append((file_dict[file_name], file_path))
            else:
                file_dict[file_name] = file_path

    return duplicate_files
