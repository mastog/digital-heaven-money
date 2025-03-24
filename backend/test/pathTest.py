import os
from backend import Config

def write_file_to_upload_dir(filename, content):
    # Get the file upload directory
    upload_dir = Config.FILE_UPLOAD_DIR

    # Construct the full file path
    file_path = os.path.join(upload_dir, filename)

    # Write the file
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"File '{filename}' written to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

# Example: Write a file
if __name__ == '__main__':
    # Example content (can be any data you want to write)
    file_content = b"Hello, this is a test file content."

    # Example filename
    file_name = "example.txt"

    # Call the function to write the file
    success = write_file_to_upload_dir(file_name, file_content)
    if success:
        print("File written successfully!")
    else:
        print("Failed to write file.")