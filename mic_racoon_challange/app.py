import os
from typing import Annotated
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .helpers import ensure_dir, save_file_to_dir, get_file_name
from .dicom_handlers import process_dicom, get_dicom_details

load_dotenv()
app = FastAPI()

UPLOAD_DIR = './uploads'
ensure_dir(UPLOAD_DIR)

app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Endpoint to provide a basic API status
@app.get("/api")
async def api():
    return {"status": "success"}


# Endpoint to get details of all processed DICOMs
@app.get("/api/dicoms/all")
async def get_all_dicoms():
    processed_dir = Path(UPLOAD_DIR, 'processed')
    dicoms_dir = processed_dir / 'dicoms'
    png_dir = processed_dir / 'pngs'
    ensure_dir(dicoms_dir)
    ensure_dir(png_dir)

    files = [f for f in os.listdir(dicoms_dir) if os.path.isfile(dicoms_dir / f)]
    all_dicoms = []
    for f in files:
        dicom_file = f'/{dicoms_dir}/{str(f)}'
        types, filename, volume = get_dicom_details('.' + dicom_file)
        item = {
            'name': filename,
            'imageTypes': types,
            'file': dicom_file,
            'volume': volume,
            'image': f'/{png_dir}/{get_file_name(f)}.png'
        }

        all_dicoms.append(item)

    return {"dicoms": all_dicoms}


# Endpoint to handle DICOM file uploads and processing
@app.post("/api/upload/")
async def create_upload_file(file: Annotated[UploadFile, File()]):
    if file.content_type != 'application/dicom':
        return {
            "filename": "",
            "volume": -1,
            "status": "failed",
        }

    threshold = float(os.environ.get('DICOM_THRESHOLD', 0.5))

    processed_dir = Path(UPLOAD_DIR, 'processed')
    ensure_dir(str(processed_dir))

    raw_dir = Path(UPLOAD_DIR, 'raw')
    ensure_dir(str(raw_dir))

    dicom_path = save_file_to_dir(str(raw_dir), file)
    volume = process_dicom(dicom_path, output_dir=str(processed_dir), threshold_val=threshold)

    return {
        "filename": file.filename,
        "volume": volume,
        "status": "success",
    }


# Endpoint to handle 404 errors
@app.get("/api/{full_path:path}")
async def not_found():
    return {"error": "not found"}


# Endpoint to serve the frontend index.html file
@app.get('/{full_path:path}')
async def index():
    return FileResponse('dist/index.html')

