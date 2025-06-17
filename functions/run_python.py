import os
import subprocess

# subprocess allows us to run python code in python code
def run_python_file(working_directory, file_path):
    original_file_path = file_path
    try:
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path.startswith(working_directory):
            return f'Error: Cannot execute "{original_file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path):
            return f'Error: File "{original_file_path}" not found'
        
        if not file_path.endswith('.py'):
            return f'Error: "{original_file_path}" is not a Python file'
        
        # Returns an object
        process = subprocess.run(['python3', file_path], 
                                 timeout=30, 
                                 capture_output=True, 
                                 text=True)

        output_parts = []

        # if strip does NOT run output_parts is FALSE, we return no output
        if process.stdout.strip():
            output_parts.append(f"STDOUT: {process.stdout.strip()}")
        if process.stderr.strip():
            output_parts.append(f"STDERR: {process.stderr.strip()}")
        if not output_parts:
            return "No output produced."
        
        # Join stuff together
        result = "/n".join(output_parts)
        if process.returncode != 0:
            result += f"\nProcess exited with code {process.returncode}" 

        return result
        
       
    except Exception as e:
        return f'Error: executing Python file: {e}'
