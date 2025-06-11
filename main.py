import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Self-note, sys is system and it can load terminal arguments. [0] is the name of the file, each argument after that follows like a list
load_dotenv()
user_prompt = sys.argv[1]

# Load the api key from the environment variable .env
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Loading the string provided at the terminal when running python3
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]
response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")