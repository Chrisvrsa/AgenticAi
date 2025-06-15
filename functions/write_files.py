import os

def write_file(working_directory, file_path, content):
    if not isinstance(content, str):
        return "Error: Content is not a string"

    try:
        working_directory = os.path.abspath(working_directory)
        file_path_absolute = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path_absolute.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # This creates a directory if it doesnt exist. exist_ok means it wont crash if the directory already exists
        os.makedirs(os.path.dirname(file_path_absolute), exist_ok=True)
        with open(file_path_absolute, 'w') as file:
            file.write(content)
            return f'Successfully wrote to \"{file_path}\" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'
        
