import shutil
from pathlib import Path
from typing import List


def copy_file(file_path: Path, destination_folder: Path):
    # Ensure the destination folder exists, create if not
    destination_folder.mkdir(parents=True, exist_ok=True)
    # Construct the new path for the file in the destination folder
    new_file_path = destination_folder / file_path.name
    # Copy the file
    shutil.copy(str(file_path), str(new_file_path))
    print(f"Copied {file_path} to {new_file_path}")


def copy_all_files(folder_dir: Path, destination_folder: Path):
    file_format = "txt"  # Adjusted to look for TXT files as per the context

    # Initialize txt_files as a list instance
    txt_files: List[Path] = []

    # Directly convert generator to list and extend txt_files
    txt_files.extend(list(folder_dir.rglob(f"*.{file_format}")))

    for file_path in txt_files:
        copy_file(file_path, destination_folder)


if __name__ == "__main__":
    folder_dir = Path("../../pecha_data")
    destination_folder = Path("../../pecha_data_txt")
    copy_all_files(folder_dir, destination_folder)
