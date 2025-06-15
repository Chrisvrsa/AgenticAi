import os
import subprocess

# subprocess allows us to run python code in python code
def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path.startswith(working_directory):
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        subprocess.run(file_path, timeout=30, capture_output=True)
        
    except Exception as e:
        return f'Error: {str(e)}'
