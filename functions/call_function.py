import os
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from google.genai import types


function_dict = {"get_files_info": get_files_info}


def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")

    name = function_call.name
    args = function_call.args
    result = None

    if name == "get_files_info":
        result = get_files_info(os.getcwd(), args.get("directory", ""))
    elif name == "write_file":
        result = write_file(
            os.getcwd(), args.get("file_path", ""), args.get("content", "")
        )
    elif name == "get_file_content":
        try:
            result = get_file_content(os.getcwd(), args.get("file_path", ""))
        except PermissionError:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={
                            "error": f"The file is not in the working directory, not enough permission to read it"
                        },
                    )
                ],
            )
        except FileNotFoundError:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={"error": f"The file was not found"},
                    )
                ],
            )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )
