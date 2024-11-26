

import os

# Input the folder path, string1, and string2
folder_path = input("Enter the folder path: ")
string1 = input("Enter the string to replace: ")
string2 = input("Enter the new string: ")

# Go through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file name contains string1
    if string1 in filename:
        # Create the new file name by replacing string1 with string2
        new_filename = filename.replace(string1, string2)
        # Get the full old and new file paths
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} -> {new_filename}')
