import os

# This bundle of joy can raise errors.😉🚒
def get_files_info(working_directory, directory=None):
    try:
    # Absolute path of the working directory
        working_directory = os.path.abspath(working_directory)

        # This represents the user wanting to view the current directory. '.' in the terminal represents the current directory
        if directory == None or directory == '.':
            final_list = []
            list_of_directories = os.listdir(working_directory)

            for file_name in list_of_directories:
                # We need to join the absolute path with the directory name. Otherwise we return main.py 🤬FUCK.
                # No one told me there's a function for that. Nvm

                joined_path = os.path.join(working_directory, file_name)
                file_size = os.path.getsize(joined_path)
                is_directory = os.path.isdir(joined_path)
                final_list.append(f'- {file_name}: file_size={file_size} bytes, is_dir={is_directory}')
            
            # join final list to a string

            return ('\n').join(final_list)
        
        # We now can store the absolute path 
        directory = os.path.abspath(os.path.join(working_directory, directory))

        # Check if the directory is inside the working directory, or print an error
        if not directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the directory is an actual directory or something else (a file, etc)
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        
        # Do the same process after these checks. This shouldn't override anything since we return at the top. The same name here is proper.

        final_list = []
        list_of_directories = os.listdir(directory)

        for file_name in list_of_directories:
            joined_path = os.path.join(directory, file_name)
            file_size = os.path.getsize(joined_path)
            is_directory = os.path.isdir(joined_path)
            final_list.append(f'- {file_name}: file_size={file_size} bytes, is_dir={is_directory}')

        return ('\n').join(final_list)

                
    except Exception as e:
        return f"Error: {str(e)}"

        
        