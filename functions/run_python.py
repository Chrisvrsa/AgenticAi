import os
import subprocess

# subprocess allows us to run python code in python code
def run_python_file(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # common errors
        if not file_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # This returns a subprocess object
        process = subprocess.run(['python3', file_path], timeout=30, capture_output=True, text=True)

        # Debug prints - add these temporarily
        print("DEBUG - stdout repr:", repr(process.stdout))
        print("DEBUG - stderr repr:", repr(process.stderr))
        print("DEBUG - returncode:", process.returncode)

        if process.stderr == "" and process.stdout == "":
            return "No output produced."

        if process.returncode == 0:
            return f"STDOUT: {process.stdout} STDERR: {process.stderr}"
        elif process.returncode != 0:
            return f"STDOUT: {process.stdout} STDERR: {process.stderr} Process exited with code {process.returncode}"
        
       

    except Exception as e:
        return f'Error: executing Python file: {e}'
