# Inspired by: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
# Made by myself, feel free to use it, please put some credits for github.com/burgil somewhere if you use it

import os

def is_file_large(file_path, threshold):
    """
    Check if a file is larger than the specified threshold size.
    """
    return os.path.getsize(file_path) > threshold

def ignore_large_files(root_dir, threshold):
    """
    Ignore files larger than the specified threshold size.
    """
    total_repo_size = 0
    ignored_size = 0
    ignored_files = 0
    total_files = 0
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if '.git' not in file_path and '.json' in file_path:
                if is_file_large(file_path, threshold):
                        print(f"Ignoring {file_path}")
                        ignored_files = ignored_files + 1
                        with open(".gitignore", "a") as gitignore:
                            gitignore.write(f"# Ignored file: {os.path.relpath(file_path, start=root_dir).replace('\\', '/')}, Size: {format_file_size(os.path.getsize(file_path))}\n")
                            gitignore.write(f"{os.path.relpath(file_path, start=root_dir).replace('\\', '/')}\n")
                        ignored_size += os.path.getsize(file_path)
                else:
                    total_files = total_files + 1
                    total_repo_size += os.path.getsize(file_path)

    return total_repo_size, ignored_size, ignored_files, total_files

def format_file_size(size):
    """
    Format file size to KB, MB, GB, TB.
    """
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    elif size < 1024 * 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
    else:
        return f"{size / (1024 * 1024 * 1024 * 1024):.2f} TB"

def get_valid_number(prompt, lower_limit, upper_limit):
    """
    Prompt the user to enter a number within the specified range.
    """
    while True:
        try:
            number = float(input(prompt))
            if number < lower_limit or number > upper_limit:
                print(f"Number must be between {lower_limit} and {upper_limit}")
            else:
                return number
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    root_directory = "."
    megabytes_limit = get_valid_number("Enter the megabytes limit: ", 1, float('inf'))
    size_threshold = megabytes_limit * 1024 * 1024

    total_repo_size, ignored_size, ignored_files, total_files = ignore_large_files(root_directory, size_threshold)
    total_repo_size_formatted = format_file_size(total_repo_size)
    ignored_size_formatted = format_file_size(ignored_size)
    all_files_formatted = format_file_size(total_repo_size+ignored_size)

    print(f"\n\n\n\nIgnored files larger than {str(megabytes_limit)}MB:")
    print(f"# Total repository size: {total_repo_size_formatted}")
    print(f"# Ignored size: {ignored_size_formatted}")
    print(f"# All files size: {all_files_formatted}")
    print(f"# Ignored files count: {ignored_files}")
    print(f"# Total files in repository: {total_files}")
    print(f"# All files count: {total_files+ignored_files}\n\n\n\n")
    existing_content = ""
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            existing_content = f.read()
    with open(".gitignore", "w") as gitignore:
        gitignore.write(f"# Ignored files larger than {str(megabytes_limit)}MB:\n")
        gitignore.write(f"# Total repository size: {total_repo_size_formatted}\n")
        gitignore.write(f"# Ignored size: {ignored_size_formatted}\n")
        gitignore.write(f"# All files size: {all_files_formatted}\n")
        gitignore.write(f"# Ignored files count: {ignored_files}\n")
        gitignore.write(f"# Total files in repository: {total_files}\n")
        gitignore.write(f"# All files count: {total_files+ignored_files}\n")
        gitignore.write("\n")
        gitignore.write(existing_content)
