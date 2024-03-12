import csv
from pathlib import Path
from typing import List


def get_all_txt_files(folder_dir: Path, dir_name: str, output_dir: Path):
    file_format = "txt"  # Only looking for RTF files
    txt_files: List[Path] = []
    # Use folder_dir instead of dir_name for Path search
    txt_files.extend(list(folder_dir.rglob(f"*.{file_format}")))

    csv_file_path = output_dir / f"{dir_name}_renamed_txt_files.csv"

    return rename_txt_files(txt_files, csv_file_path)


def rename_txt_files(file_paths: List[Path], csv_file_path: Path):
    renamed_files = []
    with open(csv_file_path, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Old Filename", "New Filename"])

        for file_path in file_paths:
            # Extracting the pecha_id and the original file name without its extension
            parts = file_path.parts
            # Assuming the first significant folder after the root is the pecha_id
            pecha_id = parts[4] if len(parts) > 1 else ""
            original_file_name = file_path.stem

            # Constructing new file name based on pecha_id and the original file name, ensuring .txt extension
            new_file_name = f"{pecha_id}_{original_file_name}.txt"
            new_file_path = file_path.with_name(
                new_file_name
            )  # This keeps the file in its original directory

            # Renaming the file
            file_path.rename(new_file_path)
            renamed_files.append(new_file_path)

            # Writing the old and new file paths to the CSV
            csvwriter.writerow([str(file_path), str(new_file_path)])

    print(f"Renamed {len(renamed_files)} files.")  # Debugging line
    return renamed_files


if __name__ == "__main__":
    folder_dir = Path("../../data/pecha_data")
    output_dir = Path("../../data")
    get_all_txt_files(folder_dir, "pecha_data", output_dir)
