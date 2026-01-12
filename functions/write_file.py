import os

def write_file(working_directory, file_path, content):
    try:
        # FILE VALIDATION LOGIC #
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to {file_path} as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to {file_path} as it is a directory'
        # END FILE VALIDATION LOGIC #

        # Make parent directories if they do not exist
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_file, mode='w') as file:
            file.write(content)
        success = f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        return success
    except Exception as e:
        return f'Error: Error writing to {file_path}'