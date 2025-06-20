import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

# self-note, sys is system and it can load terminal arguments. [0] is the name of the file, each argument after that follows like a list
load_dotenv()

user_prompt = ""
verbose = ""

if len(sys.argv) == 3:
    user_prompt = sys.argv[1]
    verbose = sys.argv[2]
else:
    user_prompt = sys.argv[1]

# load the api key from the environment variable .env
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# loading the string provided at the terminal when running python3
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# the first parameter is optional, schema only tells the AI what it can alter. We provide its working directory for safety.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    # creates a dict (JSON)
    parameters=types.Schema(
        type=types.Type.OBJECT,
        # properties in a key value pair. "directory" holds the value type of schema (blueprint.)
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# this file path is not optional. Unlike the first schema
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file within the working directory, up to 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file you want to read."
            )
        },
        required=["file_path"]
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output or any error messages.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file you want to execute"
            )
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given string content to a specified file within the working directory, creating any missing folders if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file you want to write to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content you want to write into the file"
            )
        },
        required=["file_path", "content"]

    )
)

available_functions = types.Tool(
    # list
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)
# Change system prompt here
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages, 
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt))
#//

function_call_part = response.function_calls
# If not empty?
if function_call_part:
    result = call_function(function_call_part[0], verbose=(verbose == "--verbose"))

    # Make sure result has usable content
    if not result.parts or not hasattr(result.parts[0], "function_response"):
        raise Exception("Fatal: call_function returned malformed content.")

    if verbose == "--verbose":
        print(f"-> {result.parts[0].function_response.response}")   
else:
    print(response.text)

# Verbose or not
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count


if verbose == "--verbose":
    print(response.text)
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")