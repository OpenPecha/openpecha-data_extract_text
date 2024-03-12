import csv
from pathlib import Path

from openpecha_data_extract_text.rename_pecha import get_all_txt_files


def test_get_all_txt_files():
    # Assuming get_all_txt_files is already defined and does what's intended
    folder_dir = Path("./tests/test_data/pecha_test_data/pecha")
    dir_name = "pecha_test_data"
    output_dir = Path("./tests/test_data/pecha_test_data/")
    get_all_txt_files(
        folder_dir, dir_name, output_dir
    )  # This should perform the renaming and create the CSV

    # Correcting the path for the csv_file_path and ensuring its existence is checked properly
    csv_file_path = Path(
        f"./tests/test_data/pecha_test_data/{dir_name}_renamed_txt_files.csv"
    )
    assert csv_file_path.exists(), "CSV file does not exist"

    with open(csv_file_path, newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # Read the headers first
        assert headers == [
            "Old Filename",
            "New Filename",
        ], "CSV headers do not match expected values"

        for row in csvreader:
            old_filename, new_filename = row
            # Extract pecha_id from the old filename's path
            pecha_id = Path(old_filename).parts[
                4
            ]  # Adjust the index based on actual path structure
            # Construct the expected new filename based on your naming convention
            expected_new_filename = f"{pecha_id}_{Path(old_filename).name}"
            # Check if the actual new filename (only the file name, not the path) matches the expected one
            assert (
                Path(new_filename).name == expected_new_filename
            ), f"Renaming did not work as expected for {old_filename}"

    print("Test passed: All files renamed correctly and logged in CSV.")
