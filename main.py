import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Self-note, sys is system and it can load terminal arguments. [0] is the name of the file, each argument after that follows like a list
load_dotenv()

user_prompt = ""
verbose = ""

if len(sys.argv) == 3:
    user_prompt = sys.argv[1]
    verbose = sys.argv[2]
else:
    user_prompt = sys.argv[1]

# Load the api key from the environment variable .env
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


# Loading the string provided at the terminal when running python3
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# First function schema. This tells the AI what to do. Not define the function.
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    # list
    function_declarations=[
        schema_get_files_info
    ]
)
# Change system prompt here
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages, 
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt))
#//

function_call_part = response.function_calls()
# If not empty?
if function_call_part:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
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
else:
    print(response.text)
    



