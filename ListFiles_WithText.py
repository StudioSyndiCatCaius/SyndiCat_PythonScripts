import os
from datetime import datetime
import time

def list_files_by_date(path, recursive=False):
    """
    Lists all files in the given path, sorted by last edited date.

    Args:
        path (str): The path to list files from.
        recursive (bool): Whether to search the path recursively.

    Returns:
        list: A list of tuples containing the file path and last edited timestamp.
    """
    file_dates = []

    if recursive:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                last_edited = os.path.getmtime(file_path)
                file_dates.append((file_path, last_edited))
    else:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                last_edited = os.path.getmtime(file_path)
                file_dates.append((file_path, last_edited))

    return sorted(file_dates, key=lambda x: x[1], reverse=True)

# Get the path from the user
path = input("Enter the path to list files: ")

# Ask if the user wants to search recursively
recursive = input("Search recursively? (y/n) ").lower() == 'y'

# List the files by last edited date
file_list = list_files_by_date(path, recursive)

# Print the file list
for file_path, last_edited in file_list:
    last_edited_datetime = datetime.fromtimestamp(last_edited)
    print(f"{file_path} - Last edited: {last_edited_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

# Wait for user input to close
input("Press Enter to close...")