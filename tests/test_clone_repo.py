from pathlib import Path

from openpecha_data_extract_text.clone_pecha import clone_all_git_repo, load_checkpoints


def test_clone_all_git_repo():
    all_pecha_ids = list(
        Path("./tests/test_data/pecha_test_files.txt").read_text().splitlines()
    )
    output_dir = Path("./tests/test_data/pecha_test_data/pecha")
    clone_all_git_repo(all_pecha_ids, output_dir)
    checkpoints = load_checkpoints(output_dir.parent)
    for pecha_id in all_pecha_ids:
        destination_folder = output_dir / pecha_id
        if destination_folder.exists() and list(destination_folder.rglob("*")):
            assert pecha_id in checkpoints
        else:
            assert pecha_id not in checkpoints
