import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # FILE VALIDATION LOGIC #
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        # END FILE VALIDATION LOGIC #

        command = ["python", target_file]
        if not args==None:
            command.extend(args)
        output = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if output.returncode != 0:
            output_string += f'process exited with code {output.returncode}'
        if output.stdout == None and output.stderr == None:
            output_string += f'No output produced'
        output_string += f'STDOUT: {output.stdout}'
        output_string += f'STDERR: {output.stderr}'
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"       