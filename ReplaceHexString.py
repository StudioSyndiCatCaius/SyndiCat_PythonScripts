import os

def replace_hex(file_path, source_string, new_string):
    # Open file in binary read mode
    with open(file_path, 'rb') as file:
        content = file.read()

    # Convert source and new strings to bytes
    source_bytes = source_string.encode('utf-8')
    new_bytes = new_string.encode('utf-8')

    # Check if the source string exists in the content
    if source_bytes in content:
        replaced_content = content.replace(source_bytes, new_bytes)
        # Open file in binary write mode and save the replaced content
        with open(file_path, 'wb') as file:
            file.write(replaced_content)
        print(f"Replaced all instances of '{source_string}' with '{new_string}' in {file_path}")
    else:
        print(f"Source string '{source_string}' not found in the file.")

def main():
    file_path = input("Enter the file path: ")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File at path {file_path} does not exist.")
        return

    while True:
        source_string = input("Enter the source string (or type 'exit' to quit): ")
        if source_string.lower() == 'exit':
            print("Exiting...")
            break

        new_string = input("Enter the new string: ")

        replace_hex(file_path, source_string, new_string)

if __name__ == "__main__":
    main()
