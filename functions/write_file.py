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


def write_file(working_dir, file_path, content):
    full_path = os.path.join(working_dir, file_path)
    dir_path = os.path.dirname(full_path)

    if not is_path_within_cwd_os(full_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    with open(full_path, "w") as file:
        file.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
