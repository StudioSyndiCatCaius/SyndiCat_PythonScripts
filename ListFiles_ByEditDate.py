import os
from datetime import datetime
import glob
import pyperclip
import io

def list_files():
    # Get folder path
    while True:
        folder_path = input("Enter folder path: ").strip()
        if os.path.isdir(folder_path):
            break
        print("Invalid folder path. Please try again.")

    # Normalize the folder path to ensure consistent separator handling
    folder_path = os.path.normpath(folder_path)

    # Ask about recursive search
    while True:
        recursive = input("Search recursively? (y/n): ").strip().lower()
        if recursive in ['y', 'n']:
            break
        print("Please enter 'y' or 'n'.")

    # Get file extension
    extension = input("Enter file extension (or press Enter for all files): ").strip()
    if extension and not extension.startswith('.'):
        extension = '.' + extension

    # Build search pattern
    pattern = '**/*' if recursive == 'y' else '*'
    if extension:
        pattern += extension

    # Get all files
    files = []
    try:
        for file_path in glob.glob(os.path.join(folder_path, pattern), recursive=(recursive == 'y')):
            if os.path.isfile(file_path):
                modified_time = os.path.getmtime(file_path)
                # Get the relative path after the input folder
                relative_path = os.path.relpath(file_path, folder_path)
                # Prepend * to the relative path
                display_path = os.path.join('*', relative_path)
                files.append((display_path, modified_time))
    except Exception as e:
        print(f"Error accessing files: {e}")
        input("Press Enter to exit...")
        return

    # Sort files by modified time (oldest first)
    files.sort(key=lambda x: x[1], reverse=False)

    # Prepare output for both display and clipboard
    output = io.StringIO()
    output.write("Files sorted by last modified date (oldest first):\n")
    output.write("-" * 80 + "\n")
    
    for file_path, modified_time in files:
        modified_date = datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
        line = f"{modified_date} - {file_path}\n"
        output.write(line)

    output.write(f"\nTotal files found: {len(files)}")
    
    # Get the complete output as a string
    result = output.getvalue()
    
    # Print to console
    print(result)
    
    # Copy to clipboard
    try:
        pyperclip.copy(result)
        print("\nList has been copied to clipboard!")
    except Exception as e:
        print(f"\nFailed to copy to clipboard: {e}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    list_files()