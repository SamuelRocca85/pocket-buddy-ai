import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

load_dotenv()

system_prompt = """
# Purpose

You are an Assistant that interacts with the user to answer to it's needs. You have access to external tools wich you can invoke to accomplish some of the user requests. 

If you don't find a file, you should search on subfolders and specify the exact location where you find it.

Limit every response to no more than 80 words max
"""

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Print a file content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
    ],
)


def main():
    verbose = False

    if len(sys.argv) < 2:
        print("No prompt provided")
        sys.exit(1)

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose = True

    prompt = sys.argv[1]

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    for _ in range(0, 10):
        function_call_part = response.function_calls
        if function_call_part is None:
            print("\n###### RESPONSE #######")
            print(response.text)
            break

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        else:
            print("Error: No candidates")
            sys.exit(1)

        function_response = call_function(function_call_part[0], verbose)
        messages.append(function_response)

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[available_functions],
            ),
        )

    if verbose and not response.usage_metadata is None:
        print(f"\n\nUser prompt: {prompt}")
        print(f"Request Tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response Tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
