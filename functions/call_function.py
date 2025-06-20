from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.run_python import run_python_file
from functions.write_files import write_file


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Inject the working directory
    function_args["working_directory"] = "./calculator"

    # Lookup table of available functions
    available_function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # Get the function by name
    function_to_call = available_function_map.get(function_name)

    if function_to_call is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ]
        )

    try:
        function_result = function_to_call(**function_args)
    except Exception as e:
        function_result = f"Error calling function: {str(e)}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )