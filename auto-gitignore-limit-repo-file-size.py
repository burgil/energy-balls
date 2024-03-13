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
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if is_file_large(file_path, threshold):
                print(f"Ignoring {file_path}")
                with open(".gitignore", "a") as gitignore:
                    gitignore.write(os.path.relpath(file_path, start=root_dir) + "\n")

if __name__ == "__main__":
    root_directory = "."  # Change this to specify the root directory
    size_threshold = 25 * 1024 * 1024  # 25MB threshold

    ignore_large_files(root_directory, size_threshold)
