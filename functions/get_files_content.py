import os

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    file_content_string = ""

    try:
        working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))


        if not abs_file_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r") as file:

            # read up to max characters. This variable is unneeded but im too lazy to fix it in other ares
            file_content_string = file.read(MAX_CHARS + 1)
            
            if len(file_content_string) > MAX_CHARS:
                return f'{file_content_string[:MAX_CHARS]}[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file_content_string
            
    except Exception as e:
        return f"Error: {str(e)}"
