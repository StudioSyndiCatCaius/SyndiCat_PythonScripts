import os
import zipfile

def extract_zips(folder_path):
    """
    Extracts the contents of all .zip files in the given folder path to a subfolder.

    Parameters:
    folder_path (str): The path to the folder containing the .zip files.

    Returns:
    None
    """
    subfolder_name = input("Enter the name of the subfolder to extract the ZIP contents to: ")
    subfolder_path = os.path.join(folder_path, subfolder_name)

    # Create the subfolder if it doesn't exist
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a .zip file
        if filename.endswith(".zip"):
            zip_path = os.path.join(folder_path, filename)
            print(f"Extracting {filename} to {subfolder_path}")

            # Extract the contents of the .zip file to the subfolder
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(subfolder_path)

    print("Extraction complete. Press Enter to close the script.")
    input()

# Example usage
folder_path = input("Enter the path to the folder containing the .zip files: ")
extract_zips(folder_path)