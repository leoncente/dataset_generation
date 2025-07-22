import os
import json

def read_json_file(file_path: str, file_name: str) -> dict:
    """Read a JSON file and return its content."""
    with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(file_path: str, file_name: str, data: dict):
    """Write data to a JSON file."""
    with open(os.path.join(file_path, file_name), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def exists_file(file_path: str, file_name: str) -> bool:
    """Check if a file exists."""
    return os.path.isfile(os.path.join(file_path, file_name))

def exists_or_create_folder(folder_path: str):
    """Check if a folder exists, if not, create it."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def read_all_files_in_folder(folder_path: str) -> list[str]:
    """Read all files in a folder and return their names."""
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]