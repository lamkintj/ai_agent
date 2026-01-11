import os
from config import CHAR_LIMIT

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot read {file_path} as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: {file_path}'
        with open(target_file) as file:
            file_content = file.read(CHAR_LIMIT)
            # Checking if file was truncated
            if file.read(1):
                file_content += f'[...File "{file_path}" truncated at {CHAR_LIMIT} characters]'
        return file_content
    except Exception as e:
        return f'Error: Error reading file {e}'
