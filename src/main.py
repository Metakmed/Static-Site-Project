import os
import shutil
from pathlib import Path


def validate_paths(source: Path | str, destination: Path | str) -> None:
    source = Path(source).resolve()
    destination = Path(destination).resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source does not exist: {source}")
    if source == destination:
        raise ValueError("Source and destination must be different")
    if source.is_relative_to(destination):
        raise ValueError("Source cannot be inside destination")
    if destination.is_relative_to(source):
        raise ValueError("Destination cannot be inside source")

def update_public(source: Path | str, destination: Path | str)-> None:

    if not os.path.exists(source):
        raise FileNotFoundError("File not Found")

    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    for file in os.listdir(source):
        file_path = os.path.join(source, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination)

        elif os.path.isdir(file_path):
            path_to_nested_directory_destination = os.path.join(destination, file)
            update_public(file_path, path_to_nested_directory_destination)


def main():
    project_root = Path(__file__).resolve().parent.parent
    path_to_public = project_root / "public"
    path_to_static = project_root / "static"
    validate_paths(path_to_static, path_to_public)
    update_public(path_to_static, path_to_public)
if __name__ == "__main__":
    main()
