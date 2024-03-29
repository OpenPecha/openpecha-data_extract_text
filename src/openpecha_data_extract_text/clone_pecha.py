import os
import subprocess
from multiprocessing import Pool
from pathlib import Path
from typing import List

from tqdm import tqdm


def save_corrupted_pecha(file_path: str, output_dir: Path):
    corrupted_file_path = output_dir / "pecha_progress" / "pecha_corrupted_files.txt"
    corrupted_file_path.parent.mkdir(
        parents=True, exist_ok=True
    )  # Ensure directory exists
    with open(corrupted_file_path, "a") as f:
        f.write(f"{file_path}\n")


def load_checkpoints(output_dir: Path):
    pecha_checkpoint = output_dir / "pecha_progress" / "pecha_checkpoint.txt"
    # Ensure the parent directory exists before touching the file

    if pecha_checkpoint.exists():
        return pecha_checkpoint.read_text().splitlines()

    return []


def save_checkpoint(file_checkpoint: str, output_dir: Path):
    checkpoint_file = output_dir / "pecha_progress" / "pecha_checkpoint.txt"
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    with open(checkpoint_file, "a") as f:
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
        save_checkpoint(str(repo_name), destination_folder.parent.parent)

    except subprocess.CalledProcessError as e:
        error_message = e.stderr  # Capture the standard error output
        print(f"[ERROR]: Error cloning {repo_name} repository: {error_message}")
        save_corrupted_pecha(
            f"{repo_name}-{error_message}", destination_folder.parent.parent
        )


def worker_task(args):
    pecha_id, output_dir, checkpoints = args
    if f"{str(pecha_id)}" in checkpoints:
        return
    clone_github_repo(pecha_id, destination_folder=output_dir)


def clone_all_git_repo(all_pecha_ids: List[str], output_dir: Path):
    checkpoints = load_checkpoints(output_dir.parent)
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
    all_pecha_ids = list(Path("../../data/pecha_files.txt").read_text().splitlines())
    output_dir = Path("../../data/pecha_data")
    clone_all_git_repo(all_pecha_ids, output_dir)
