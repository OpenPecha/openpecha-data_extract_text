import os
import subprocess
from multiprocessing import Pool
from pathlib import Path
from typing import List

from tqdm import tqdm

PECHA_CORRUPTED_FILES = Path("../../pecha_corrupted_files.txt")
if not PECHA_CORRUPTED_FILES.exists():
    PECHA_CORRUPTED_FILES.touch()


def save_corrupted_pecha(file_path: str):
    with open(PECHA_CORRUPTED_FILES, "a") as f:
        f.write(f"{file_path}\n")


"""check point system"""

PECHA_CLONED_CHECKPOINT = Path("../../pecha_checkpoint.txt")


def load_checkpoints():
    if PECHA_CLONED_CHECKPOINT.exists():
        return PECHA_CLONED_CHECKPOINT.read_text().splitlines()

    PECHA_CLONED_CHECKPOINT.touch()
    return []


def save_checkpoint(file_checkpoint: str):
    with open(PECHA_CLONED_CHECKPOINT, "a") as f:
        f.write(f"{file_checkpoint}\n")


def clone_github_repo(repo_name: str, destination_folder: Path):
    # Retrieve GitHub token and organization name from environment variables
    token = os.getenv("GITHUB_TOKEN")
    org_name = os.getenv("GITHUB_ORG")

    if not token or not org_name:
        print(
            "[ERROR]: GitHub token or organization name not found in environment variables."
        )
        return

    if destination_folder.exists() and list(destination_folder.rglob("*")):
        print(
            f"[INFO]: Destination folder {destination_folder} already exists and is not empty."
        )
        return

    try:
        # Construct the URL with authentication token
        repo_url = f"https://{token}@github.com/{org_name}/{repo_name}.git"

        # Run the git clone command
        subprocess.run(
            ["git", "clone", repo_url, str(destination_folder)],
            check=True,
            capture_output=True,
            text=True,  # Ensure output is in text format, not bytes
        )
        print(
            f"[SUCCESS]: Repository {repo_name} cloned successfully to {destination_folder}."
        )
        save_checkpoint(str(repo_name))

    except subprocess.CalledProcessError as e:
        error_message = e.stderr  # Capture the standard error output
        print(f"[ERROR]: Error cloning {repo_name} repository: {error_message}")
        save_corrupted_pecha(f"{repo_name}-{error_message}")


def worker_task(args):
    pecha_id, output_dir, checkpoints = args
    if f"{str(pecha_id)}" in checkpoints:
        return
    clone_github_repo(pecha_id, output_dir)


def clone_all_git_repo(all_pecha_ids: List[str], output_dir: Path):
    checkpoints = load_checkpoints()
    tasks = [
        (pecha_id, Path(f"{output_dir}/{pecha_id}"), checkpoints)
        for pecha_id in all_pecha_ids
    ]

    num_processes = 5
    with Pool(processes=num_processes) as pool:
        list(
            tqdm(
                pool.imap(worker_task, tasks), total=len(tasks), desc="Cloning git repo"
            )
        )


if __name__ == "__main__":
    all_pecha_ids = List(Path("../../pecha_files.txt").read_text().splitlines())
    output_dir = Path("../../pecha_data")
    clone_all_git_repo(all_pecha_ids, output_dir)
