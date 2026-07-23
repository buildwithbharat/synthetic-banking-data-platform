from pathlib import Path


def create_directory(path: str) -> None:
    """
    Creates a directory if it does not already exist.
    """
    Path(path).mkdir(parents=True, exist_ok=True)