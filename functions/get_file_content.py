import os


def is_path_within_cwd_os(target_path):
    """
    Checks if a given target_path is within the current working directory.
    Uses the os.path module.
    """
    current_working_directory = os.getcwd()
    absolute_target_path = os.path.abspath(target_path)

    # Normalize paths to handle inconsistencies like trailing slashes
    normalized_cwd = os.path.normpath(current_working_directory)
    normalized_target_path = os.path.normpath(absolute_target_path)

    return normalized_target_path.startswith(normalized_cwd)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    if not is_path_within_cwd_os(full_path):
        # print(
        #     f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        # )
        raise PermissionError(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )

    if not os.path.isfile(full_path):
        # print(f'Error: File not found or is not a regular file: "{file_path}"')
        raise FileNotFoundError(
            f'Error: File not found or is not a regular file: "{file_path}"'
        )

    MAX_CHARS = 10000

    with open(full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if len(file_content_string) == 10000:
            file_content_string += (
                f'...File "{full_path}" truncated at 10000 characters'
            )

    return file_content_string
