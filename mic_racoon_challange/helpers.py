from typing import Union
import os
from pathlib import Path
import shutil
from fastapi import File


# Function to ensure the existence of a directory
def ensure_dir(path: Union[str, Path]):
    """
    Ensure that the directory at the given path exists,
    and create it if it doesn't.

    Parameters:
    path (Union[str, Path]): Path to the directory.
    """
    is_exist = os.path.exists(path)
    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(path, mode=0o777)
    return


# Function to save a file to a directory
def save_file_to_dir(path: str, file: File) -> str:
    """
    Save the uploaded file to the specified directory.

    Parameters:
    path (str): Path to the directory where the file should be saved.
    file (File): The file to be saved.

    Returns:
    str: Path to the saved file.
    """
    output_dir = Path(path)
    outfile = output_dir / file.filename

    # Remove old file if a file with the same name exists
    # to overwrite with the new file
    if os.path.isfile(outfile):
        os.remove(outfile)

    with open(outfile, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(outfile)


# Function to get the file name from a file path
def get_file_name(filepath: str):
    """
    Extract the file name (excluding extension) from a given file path.

    Parameters:
    filepath (str): The file path.

    Returns:
    str: The file name without the extension.
    """
    return Path(filepath).stem
