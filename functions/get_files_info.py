import os
import sys


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


def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)

    if not os.path.isdir(full_path):
        print(f'Error: "{directory}" is not a directory')
        sys.exit(1)

    if not is_path_within_cwd_os(full_path):
        print(
            f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
        )
        sys.exit(1)

    entries = os.listdir(full_path)

    # print(f"Result for {directory} directory")
    result = ""

    for entry in entries:
        full_file_path = os.path.join(full_path, entry)
        name = os.path.basename(full_file_path)
        size = os.path.getsize(full_file_path)
        is_dir = os.path.isdir(full_file_path)

        result += f"- {name}: file_size={size}, is_dir={is_dir}"

    return result
