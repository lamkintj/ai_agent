import os
import subprocess
from google import genai
from google.genai import types

# Google-genai schema for calling function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run Python file located in the specified working directory. Process should return any non-zero return codes, and standard output or standard error if they exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of file to be run and its path relative to the working directory. Should be a Python file ending in .py",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of optional arguments to run with the command. Defaults to None.",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional argument supplied to command to run with Python.",
                )
            )
        },
        required=["file_path"],
    ),
)
#

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