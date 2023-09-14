from typing import Union
import os
from pathlib import Path
import shutil
from fastapi import File


def ensure_dir(path: Union[str, Path]):
    is_exist = os.path.exists(path)
    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(path, mode=0o777)
    return


def save_file_to_dir(path: str, file: File) -> str:
    output_dir = Path(path)
    outfile = output_dir / file.filename
    # remove old file if a file with same name exists
    # to overwrite with new file
    if os.path.isfile(outfile):
        os.remove(outfile)
    with open(outfile, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return str(outfile)


def get_file_name(filepath: str):
    return Path(filepath).stem
